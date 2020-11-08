from discord_webhook import DiscordWebhook, DiscordEmbed
import sched, time
from threading import Thread
import urllib.request
import hashlib

HTTP_TIMEOUT = 10

class Edt(Thread):
    _scheduler = None
    _webhook = None
    _EDT_WEBHOOK= "example.com"
    _EDT_REFRESH = 10
    _URL_ENT = "example.com"
    _lastcheck = None
    def __init__(self,EDT_WEBHOOK,EDT_REFRESH,URL_ENT):
        Thread.__init__(self)

        self._EDT_WEBHOOK = EDT_WEBHOOK
        self._EDT_REFRESH = EDT_REFRESH
        self._URL_ENT = URL_ENT
        MENTION = {
            'parse':["everyone"]
        }
        self._webhook = DiscordWebhook(url=EDT_WEBHOOK,allowed_mentions=MENTION);

        self._scheduler = sched.scheduler(time.time,time.sleep)


    def run(self):
        self._scheduler.enter(self._EDT_REFRESH,1,self._main)
        print("webhooks.Edt : démarage")
        self._scheduler.run()

    def _main(self):

        #Trucs
        print(f'[{time.asctime(time.localtime())}] Téléchargement du fichier EDT')
        try:
            with urllib.request.urlopen(self._URL_ENT,timeout=HTTP_TIMEOUT) as f:
                newedt = f.read().decode('utf-8')
        except:
            print("\tErreur au téléchargement de l'edt")
        else:
            print("\tSomme de controle md5 du fichier téléchargé")
            newcheck = hashlib.md5(newedt.encode()).hexdigest()
            print(f'\t{newcheck}')

            if(newcheck != self._lastcheck):
                if(self._lastcheck != None):
                    self._webhook.content = "@everyone"
                    embed = DiscordEmbed(title='Emploi du temps',description="L'emploi du temps à changé")
                    self._webhook.add_embed(embed);
                    self._webhook.execute();
                self._lastcheck = newcheck

        self._scheduler.enter(self._EDT_REFRESH,1,self._main)

    def test_msg(self):
        embed = DiscordEmbed(title='Test',description="Ceci est un test")
        self._webhook.content="@everyone"
        self._webhook.add_embed(embed);
        self._webhook.execute();

if __name__ == '__main__':
    EDT_WEBHOOK = ["https://discordapp.com/api/webhooks/773570005231992844/4kUhrydLzTfNECRl1Nrmo8pJWzbr8iXgUj72zUaJ8kbfTKVDIIg4qr6Vp258bGlafYlJ"]
    EDT_REFRESH = 10 #time to refresh in s
    URL_ENT = "https://dptinfo.iutmetz.univ-lorraine.fr/lna/agendas/ical.php?ical=409522f49102191"

    wb=Edt(EDT_WEBHOOK,EDT_REFRESH,URL_ENT)
    #wb.test_msg()
    wb.start()
    pass
