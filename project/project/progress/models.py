from django.db import models
from django.contrib.auth.models import User

from BeautifulSoup import BeautifulSoup as Soup
from soupselect.soupselect import select
import urllib
from urlparse import urlparse, parse_qs
from decimal import *

LANGS = ('de','en',)

class Curriculum(models.Model):
    name = models.CharField(max_length=100)
    trees = models.ManyToManyField('LVATree')
    number = models.CharField(max_length=100)
    min_ects = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    @models.permalink
    def get_absolute_url(self):
        return ('project.progress.views.curriculum', (), {'pk': self.pk},)

    def __unicode__(self):
        return u'Curriculum: %s (%s)' % (self.name, self.min_ects,)

    def decorate(self, certificates):
        trees = [tree.decorate(certificates) for tree in self.trees.all()]
        matched = set(reduce(lambda x,y:x+y, [x['matching'] for x in trees], []))
        unmatched = set(certificates) - matched
        lvas = set(reduce(lambda x,y:x+y, [x['lvas'] for x in trees], []))
        matched_ects = reduce(lambda x,y:x+y, [x.ects for x in matched], 0)
        return {'name': self.name, 'trees': trees, 'min_ects': self.min_ects, 'number': self.number,
                'unmatched': unmatched, 'matched_ects': matched_ects}

    @classmethod
    def parse_from_curriculum_url(cls,url):
        soup = Soup(urllib.urlopen(url))

        levelindex = 0
        previous_levelindex = -1
        curriculum = None
        stack = []
        obj = None

        if 'errorPage' in soup:
            print 'error page!'
            return

        titles = [x.text for x in select(soup, 'h1') if x.text]


        currno = ''.join(titles[0].strip().split(' ',2)[:2])
        name = ''.join(titles[0].strip().split(' ',2)[2:])


        lang = dict(select(soup, 'body')[0].attrs)['class'].replace('lehre','').strip()

        if lang!='de':
            print 'import not german'
            return

        for x in select(soup, '#nodeTable tbody tr'):
            data = select(x, 'td')
            title = data[0]
            (smst, ects) = data[-2:]

            ects = ects.text
            if ects:
                ects = Decimal(ects)

            titlelevel = dict(select(title, 'div')[0].attrs)['class'].replace('nodeTable-level-','')

            levelindex = int(titlelevel[0], 10)

            if previous_levelindex > levelindex and stack and levelindex<3:
                number = previous_levelindex if previous_levelindex < 4 else 3
                for x in range(levelindex, number):
                    stack.pop()

            if levelindex == 0:
                curriculum, created = Curriculum.objects.get_or_create(name=name, number=currno)
                if not created:
                    curriculum.trees.all().delete()
            if levelindex == 1:
                name = select(title, 'span')[0].text
                type_ = title.text[:-len(name)]
                if title.text.startswith('Curriculum Suppleme'):
                    print type_
                    break
                lvatree = LVATree.objects.create(treetype=type_, name=name, min_ects=ects if ects else 0)
                if stack:
                    stack[-1].subtrees.add(lvatree)
                else:
                    curriculum.trees.add(lvatree)
                stack.append(lvatree)
            if levelindex == 2:
                name = select(title, 'span')[0].text
                type_ = title.text[:-len(name)]
                lvatree = LVATree.objects.create(treetype=type_, name=name, min_ects=ects if ects else 0)
                if stack:
                    stack[-1].subtrees.add(lvatree)
                else:
                    curriculum.trees.add(lvatree)
                stack.append(lvatree)
            if levelindex == 3:
                courseTitle = select(title, 'span')[0].text.strip()
                courseType = title.text.strip()[:2]
                if not ects:
                    print 'ignored: ', courseTitle
                    continue
                lva = LVA.objects.create(lvatype = courseType, ects=ects, name_de = courseTitle)
                stack[-1].lvas.add(lva)
            if levelindex == 4:
                pass

            previous_levelindex = levelindex
        return curriculum

    @classmethod
    def parse_from_text(self, text):
        pass

class LVA(models.Model):
    lvatype = models.CharField(max_length=3)
    name_de = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True, blank=True)
    ects = models.DecimalField(max_digits=4, decimal_places=2)

    @property
    def name(self):
        return self.name_de

    def __unicode__(self):
        return u'LVA: %s %s (%s)' % (self.lvatype, self.name, self.ects,)

    def decorate(self, certificates):
        matching = [cert for cert in certificates if self.name==cert.lvaname_de and self.lvatype==cert.lvatype]
        return {'name': self.name, 'type': self.lvatype, 'ects': self.ects, 'matching': matching}

class LVATree(models.Model):
    lvas = models.ManyToManyField(LVA)
    subtrees = models.ManyToManyField('LVATree')
    treetype = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    min_ects = models.DecimalField(max_digits=4, decimal_places=2, null=True)

    def __unicode__(self):
        return u'%s %s (%s)' % (self.treetype or '', self.name or '', self.min_ects,)

    def decorate(self, certificates):
        lvas = [lva.decorate(certificates) for lva in self.lvas.all()]
        trees = [tree.decorate(certificates) for tree in self.subtrees.all()]
        matching = reduce(lambda x,y: x + y, [x['matching'] for x in lvas] + [x['matching'] for x in trees], [])
        if len(matching) != len(set(matching)):
            print 'zomgmatchingerror!'
            print matching
        ects = reduce(lambda x,y: x+y, [x['ects'] for x in lvas if x['matching']] + [y['ects'] for y in trees], Decimal(0))
        return {'name': self.name, 'type': self.treetype, 'trees': trees, 'min_ects': self.min_ects, 'lvas': lvas, 'matching': matching, 'ects': ects, 'complete': ects>=self.min_ects}

class Certificate(models.Model):
    lvano = models.CharField(max_length=100)
    lvatype = models.CharField(max_length=100)
    lvaname_import = models.CharField(max_length=100)
    lvaname_de = models.CharField(max_length=100)
    lvaname_en = models.CharField(max_length=100)
    semst = models.DecimalField(max_digits=4,decimal_places=2)
    ects = models.DecimalField(max_digits=4,decimal_places=2)
    date = models.CharField(max_length=100)
    curriculum = models.CharField(max_length=100)
    mark = models.CharField(max_length=100,null=True,blank=True)
    professor = models.CharField(max_length=100,null=True,blank=True)
    user = models.ForeignKey(User)
    use_for = models.ForeignKey(Curriculum, null=True, blank=True)
    #use_for_tree = models.CharField(max_length=100, null=True, blank=True)


    @property
    def whichcurriculum(self):
        return self.use_for if self.use_for else self.curriculum
    
    @property
    def curriculum_overridden(self):
        return self.use_for

    class Meta:
        unique_together = [('lvano', 'user',)]

    def __unicode__(self):
        return u'%s (%s %s)' % (self.lvaname_de, self.ects, self.use_for,)

    @classmethod
    def create(cls, user, **data):
        data['lvano'] = ''.join([x for x in data['lvano'] if x.isalnum()])

        url = 'https://tiss.tuwien.ac.at/course/courseDetails.xhtml?courseNr='+data['lvano']
        url_de = url + '&locale=de'
        url_en = url + '&locale=en'
        soup_de = Soup(urllib.urlopen(url_de))
        soup_en = Soup(urllib.urlopen(url_en))

        remove_spans = lambda x: x.text.replace(select(x, 'span')[0].text,'').strip()
        get_name = lambda s: remove_spans([x for x in select(s, 'h1') if x.text][0])
        data['lvaname_de'] = get_name(soup_de)
        data['lvaname_en'] = get_name(soup_en)
        data['lvaname_import'] = data['lvaname'].strip()
        if data['lvaname'] not in (data['lvaname_de'],data['lvaname_en'], ):
            print data['lvaname'], 'is not the same as', data['lvaname_de'], data['lvaname_en']
            return
        del data['lvaname']
        try:
            x = Certificate.objects.get(lvano=data['lvano'], user=user)
            print x, 'cert already exists'
        except Certificate.DoesNotExist:
            return Certificate.objects.create(user=user, **data)

