from dj_server.quickstart.models import Hero

hero_1 = Hero(name="Superman", alias="SM")
hero_2 = Hero(name="Batman", alias="BM")

hero_1.save()
hero_2.save()
