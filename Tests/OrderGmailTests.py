import unittest
import OrderGmail
from models import Person


class OrderGmailTests(unittest.TestCase):
    def test_decode_mail_str(self):
        encoded_str = "PGRpdj48ZGl2IHN0eWxlPSJiYWNrZ3JvdW5kLWNvbG9yOnJnYiggMjU1ICwgMjU1ICwgMjU1ICk7Y29sb3I6cmdiKCAzNCAsIDM0ICwgMzQgKTtmb250LWZhbWlseTonYXJpYWwnICwgJ2hlbHZldGljYScgLCBzYW5zLXNlcmlmO2ZvbnQtc2l6ZTpzbWFsbDtmb250LXN0eWxlOm5vcm1hbDtmb250LXdlaWdodDo0MDA7dGV4dC1kZWNvcmF0aW9uLXN0eWxlOmluaXRpYWw7dGV4dC1pbmRlbnQ6MHB4O3RleHQtdHJhbnNmb3JtOm5vbmU7d2hpdGUtc3BhY2U6bm9ybWFsO3dvcmQtc3BhY2luZzowcHgiPm5hbWU90JjRgdGC0L7Rh9C90LjQuiDQotC10YHRgiDQotC10YHRgtC-0LLQuNGHPC9kaXY-PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjpyZ2IoIDI1NSAsIDI1NSAsIDI1NSApO2NvbG9yOnJnYiggMzQgLCAzNCAsIDM0ICk7Zm9udC1mYW1pbHk6J2FyaWFsJyAsICdoZWx2ZXRpY2EnICwgc2Fucy1zZXJpZjtmb250LXNpemU6c21hbGw7Zm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6NDAwO3RleHQtZGVjb3JhdGlvbi1zdHlsZTppbml0aWFsO3RleHQtaW5kZW50OjBweDt0ZXh0LXRyYW5zZm9ybTpub25lO3doaXRlLXNwYWNlOm5vcm1hbDt3b3JkLXNwYWNpbmc6MHB4Ij5waG9uZT0yMjIzMzIyPC9kaXY-PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjpyZ2IoIDI1NSAsIDI1NSAsIDI1NSApO2NvbG9yOnJnYiggMzQgLCAzNCAsIDM0ICk7Zm9udC1mYW1pbHk6J2FyaWFsJyAsICdoZWx2ZXRpY2EnICwgc2Fucy1zZXJpZjtmb250LXNpemU6c21hbGw7Zm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6NDAwO3RleHQtZGVjb3JhdGlvbi1zdHlsZTppbml0aWFsO3RleHQtaW5kZW50OjBweDt0ZXh0LXRyYW5zZm9ybTpub25lO3doaXRlLXNwYWNlOm5vcm1hbDt3b3JkLXNwYWNpbmc6MHB4Ij5lbWFpbD1pc3RvY2huaWstc3BiQHlhbmRleC5ydTwvZGl2PjxkaXYgc3R5bGU9ImJhY2tncm91bmQtY29sb3I6cmdiKCAyNTUgLCAyNTUgLCAyNTUgKTtjb2xvcjpyZ2IoIDM0ICwgMzQgLCAzNCApO2ZvbnQtZmFtaWx5OidhcmlhbCcgLCAnaGVsdmV0aWNhJyAsIHNhbnMtc2VyaWY7Zm9udC1zaXplOnNtYWxsO2ZvbnQtc3R5bGU6bm9ybWFsO2ZvbnQtd2VpZ2h0OjQwMDt0ZXh0LWRlY29yYXRpb24tc3R5bGU6aW5pdGlhbDt0ZXh0LWluZGVudDowcHg7dGV4dC10cmFuc2Zvcm06bm9uZTt3aGl0ZS1zcGFjZTpub3JtYWw7d29yZC1zcGFjaW5nOjBweCI-aXNfY3VzdG9tZXI9PHN0cm9uZz5UcnVlPC9zdHJvbmc-PC9kaXY-PGRpdiBzdHlsZT0iYmFja2dyb3VuZC1jb2xvcjpyZ2IoIDI1NSAsIDI1NSAsIDI1NSApO2NvbG9yOnJnYiggMzQgLCAzNCAsIDM0ICk7Zm9udC1mYW1pbHk6J2FyaWFsJyAsICdoZWx2ZXRpY2EnICwgc2Fucy1zZXJpZjtmb250LXNpemU6c21hbGw7Zm9udC1zdHlsZTpub3JtYWw7Zm9udC13ZWlnaHQ6NDAwO3RleHQtZGVjb3JhdGlvbi1zdHlsZTppbml0aWFsO3RleHQtaW5kZW50OjBweDt0ZXh0LXRyYW5zZm9ybTpub25lO3doaXRlLXNwYWNlOm5vcm1hbDt3b3JkLXNwYWNpbmc6MHB4Ij5pc19wZXJmb3JtZXI9PC9kaXY-PC9kaXY-PGRpdj7CoDwvZGl2PjxkaXY-LS3CoDxiciAvPtChINGD0LLQsNC20LXQvdC40LXQvCw8L2Rpdj48ZGl2PtCR0LXQt9C70Y7QtNC90YvQuSDQkNC70LXQutGB0LXQuTwvZGl2PjxkaXY-KDgxMikgOTIwLTQ4LTI0PC9kaXY-PGRpdj7CoDwvZGl2Pg=="
        source_str ='<div><div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 34 , 34 , 34 );font-family:\'arial\' , \'helvetica\' , sans-serif;font-size:small;font-style:normal;font-weight:400;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">name=Источник Тест Тестович</div><div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 34 , 34 , 34 );font-family:\'arial\' , \'helvetica\' , sans-serif;font-size:small;font-style:normal;font-weight:400;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">phone=2223322</div><div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 34 , 34 , 34 );font-family:\'arial\' , \'helvetica\' , sans-serif;font-size:small;font-style:normal;font-weight:400;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">email=istochnik-spb@yandex.ru</div><div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 34 , 34 , 34 );font-family:\'arial\' , \'helvetica\' , sans-serif;font-size:small;font-style:normal;font-weight:400;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">is_customer=<strong>True</strong></div><div style="background-color:rgb( 255 , 255 , 255 );color:rgb( 34 , 34 , 34 );font-family:\'arial\' , \'helvetica\' , sans-serif;font-size:small;font-style:normal;font-weight:400;text-decoration-style:initial;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px">is_performer=</div></div><div> </div><div>-- <br />С уважением,</div><div>Безлюдный Алексей</div><div>(812) 920-48-24</div><div> </div>'

        decoded_str = OrderGmail.decode_mail_str(encoded_str)

        self.assertTrue(len(decoded_str) > 0)
        self.assertEqual(source_str, decoded_str)

    def test_create_sql_insert_message(self):
        result1 = {'ok': True, 'person': Person() }
        result2 = {'ok': False, 'person': Person()}
        results = [result1, result2]
        message = OrderGmail.create_sql_insert_message(results)
        lines = message.splitlines()
        self.assertEqual(4, len(lines))

    def test2_create_sql_insert_message(self):
        results = None
        message = OrderGmail.create_sql_insert_message(results)
        lines = message.splitlines()

        self.assertEqual(1, len(lines))
        self.assertEqual('Ошибка добавления в Базу данных ', lines[0])


if __name__ == '__main__':
    unittest.main()
