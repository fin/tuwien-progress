/* */

function extractCerts() {
    var certs = [];
    var labels = ['lvano', 'lvatype', 'lvaname', 'semst', 'ects', 'date', 'curriculum', 'mark', 'professor'];
    var rows = document.querySelectorAll('#certificateList\\:certificatesPanel table tbody')[0].childNodes;
    for(var j=0;j<rows.length;j++) {
        var row = rows[j];
        var cert = {};
        for(var i=0;i<labels.length;i++) {
            cert[labels[i]] = row.childNodes[i].childNodes[0].innerHTML; /* the 2nd childNodes[0] just ignores a span element */
        }
        certs.push(cert);
    }
    return certs;
}

function sendCerts() {
    var certs = extractCerts();

    $.post('https://nomin.at/p/tiss/cert/?auth_token='+window.tisshack_authkey, certs);
}

if($===undefined) {
    var s=document.createElement('script');
    s.setAttribute('src','//ajax.googleapis.com/ajax/libs/jquery/1.4.3/jquery.min.js');
    document.getElementsByTagName('body')[0].appendChild(s);
    setTimeout(sendCerts, 2000);
} else {
    sendCerts();
}


