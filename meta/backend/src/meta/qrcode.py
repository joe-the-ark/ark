
from django.utils.six import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

import qrcode


def make_qrcode(url, name='qr.png'):
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf)
    qr_data = buf.getvalue()
    buf.write(qr_data)
    qr_img = InMemoryUploadedFile(file=buf, field_name=None, name=name, content_type='image/png',
        size=len(qr_data), charset=None)

    return qr_img