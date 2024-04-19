from django.templatetags.static import static

from store.core.metadata import Metadata

metadata = Metadata(
    title='อควาเรียส',
    shortcut_icon=static('store/img/favicon.ico'),
    og_type='website',
    og_description='ร้านขายหนังสือการ์ตูน ไลท์โนเวล มังงะ และสินค้าอื่นๆ',
    og_image=static('store/img/favicon.png'),
)
