import haravasto
from random import *
import time
import os


def luo_kentta():
    """Luo kentän käyttäjän syöttämillä arvoilla"""
    while True:
        try:
            pituus = int(input("Anna kentän pituus: "))
            if pituus < 3 or pituus > 100:
                print("Kentän pituus on vähintään 3 ja enintään 100")
                raise ValueError
            korkeus = int(input("Anna kentän korkeus: "))
            if korkeus < 3 or korkeus > 100:
                print("Kentän korkeus on vähintään 3 ja enintään 100")
                raise ValueError
            miinojen_lkm = int(input("Anna miinojen lukumäärä: "))
            if miinojen_lkm < 1 or miinojen_lkm >= pituus * korkeus:
                print("Miinojen määrä on vähintään 1 ja enintään yksi vähemmän kuin ruutuja!")
                raise ValueError
            break
        except ValueError:
            print("Väärä syöte!")

    kentta = []
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(pituus):
            kentta[-1].append(" ")

    jaljella = []
    for x in range(pituus):
        for y in range(korkeus):
            jaljella.append((x, y))

    miinoita(kentta, jaljella, miinojen_lkm)

    statistiikka["kentan_korkeus"] = korkeus
    statistiikka["kentan_pituus"] = pituus
    statistiikka["miinojenlkm"] = miinojen_lkm

    return kentta


def miinoita(kentta, vapaat_ruudut, miinojen_lkm):
    """Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin."""

    while miinojen_lkm > 0:
        koko = len(vapaat_ruudut) - 1
        rand = randint(0, koko)
        x, y = vapaat_ruudut[rand][:]
        kentta[y][x] = "x"
        vapaat_ruudut.remove(vapaat_ruudut[rand])
        miinojen_lkm = miinojen_lkm - 1


def tulvataytto(kentta, x, y):
    """Merkitsee kentällä olevat tuntemattomat alueet turvalliseksi siten,
    että täyttö aloitetaan annetusta x, y -pisteestä."""
    lista = [(x, y)]
    if kentta[y][x] == " ":
        while len(lista) > 0:
            koordinaatit = lista.pop()
            x = int(koordinaatit[0])
            y = int(koordinaatit[1])
            if 0 == laske_miinat(x, y, kentta):
                kentta[y][x] = "0"
            else:
                kentta[y][x] = str(laske_miinat(x, y, kentta))
                continue

            for i in range(y - 1, y + 2):
                for j in range(x - 1, x + 2):
                    if i < 0:
                        i = 0
                    if j < 0:
                        j = 0
                    if j > len(kentta[0]) - 1:
                        j = len(kentta[0]) - 1
                    if i > len(kentta) - 1:
                        i = len(kentta) - 1
                    if kentta[i][j] == " ":
                        pituus = j
                        korkeus = i
                        uusik = (pituus, korkeus)
                        lista.append(uusik)


def laske_miinat(x, y, kentta):
    """Laskee yhden ruudun ympärillä olevat miinat ja palauttaa niiden lukumäärän"""
    yhteensa = 0
    for i in range(y - 1, y + 2):
        for j in range(x - 1, x + 2):
            if tarkista_koordinaatit(j, i, len(kentta[1]), len(kentta)):
                if kentta[i][j] == "x":
                    yhteensa = yhteensa + 1
    return yhteensa


def kasittele_hiiri(x, y, painike, muokkausnapit):
    """Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Tulostaa hiiren sijainnin sekä painetun napin terminaaliin."""

    if painike == haravasto.HIIRI_VASEN:
        x_koordinaatti = int(x / 40)
        y_koordinaatti = int(y / 40)
        statistiikka["siirtojen_lkm"] = statistiikka["siirtojen_lkm"] + 1
        pelilogiikka(x_koordinaatti, y_koordinaatti)


def tallenna_statistiikka(statistiikka):
    "Tallentaa pelin tiedot tiedostoon"

    with open("miinaharava.txt", "a") as tiedosto:
        tiedosto.write("\n**********\nPelin ajankohta: {}\nPelin kesto: {}\nSiirtojen lukumäärä: {}\n"
                       "Pelitilanne: {}\nKentän koko: {} x {}\nMiinojen lukumäärä: {}\n**********\n".format(
            statistiikka["aika"],
            statistiikka["kesto"], statistiikka["siirtojen_lkm"], statistiikka["peli_tilanne"],
            statistiikka["kentan_pituus"], statistiikka["kentan_korkeus"], statistiikka["miinojenlkm"]))


def lue_statistiikka():
    "Lukee ja tulostaa edellisten pelien tiedot tiedostosta"
    with open("miinaharava.txt") as tiedosto:
        tiedot = tiedosto.read()
        print(tiedot)


def pelilogiikka(x_koordinaatti, y_koordinaatti):
    "Ohjelman tärkein funktio jossa pelin kulkua hallitaan"
    if tarkista_koordinaatit(x_koordinaatti, y_koordinaatti, len(kentta[1]), len(kentta)):
        if kentta[y_koordinaatti][x_koordinaatti] == " ":
            if 0 == laske_miinat(x_koordinaatti, y_koordinaatti, kentta):
                tulvataytto(kentta, x_koordinaatti, y_koordinaatti)
            else:
                kentta[y_koordinaatti][x_koordinaatti] = str(laske_miinat(x_koordinaatti, y_koordinaatti, kentta))

        if onko_tyhjaa(kentta):
            print("Onneksi olkoon! Voitit pelin!")
            statistiikka["peli_tilanne"] = "Voitto"
            statistiikka["peli_paattyi"] = True
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri_lopetus)

        if kentta[y_koordinaatti][x_koordinaatti] == "x":
            kentta[y_koordinaatti][x_koordinaatti] = "m"
            print("Hävisit pelin!")
            statistiikka["peli_paattyi"] = True
            statistiikka["peli_tilanne"] = "Häviö"
            haravasto.aseta_hiiri_kasittelija(kasittele_hiiri_lopetus)


def onko_tyhjaa(kentta):
    "Tarkistetaan onko tarkistamattomia ruutuja"
    for i in kentta:
        for j in i:
            if j == " ":
                return
    return True


def kasittele_hiiri_lopetus(x, y, painike, muokkausnapit):
    "Tämä funktio sulkee ikkunan pelin jälkeen vasemmalla hiiren näppäimellä"
    aika_loppu = time.time()
    statistiikka["kesto"] = time.strftime("%M min %S s", time.gmtime(aika_loppu - aika_alku))
    if haravasto.HIIRI_VASEN:
        tallenna_statistiikka(statistiikka)
        haravasto.lopeta()


def tarkista_koordinaatit(x, y, leveys, korkeus):
    """Tarkistaa ovatko annetut x, y -koordinaatit annettujen rajojen sisällä.
    Palauttaa True, jos koordinaatit ovat rajojen sisällä; muuten palautetaan False."""

    try:
        if x < 0 or y < 0:
            raise TypeError
        if x >= 0 and x < leveys and y >= 0 and y < korkeus:
            return True
        else:
            return False
    except TypeError:
        return False


def piirra_kentta():
    """Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun
    miinakentän ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori
    pyytää ruudun näkymän päivitystä."""
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()

    y = -40
    for i in kentta:
        y = y + 40
        x = - 40
        for j in i:
            x = x + 40
            haravasto.lisaa_piirrettava_ruutu(" ", x, y)
            if j == "f":
                haravasto.lisaa_piirrettava_ruutu("f", x, y)
            if j == "m":
                haravasto.lisaa_piirrettava_ruutu("x", x, y)
            for k in range(9):
                k = str(k)
                if k == j:
                    haravasto.lisaa_piirrettava_ruutu(k, x, y)
            if statistiikka["peli_paattyi"]:
                if j == "x" or j == "m":
                    haravasto.lisaa_piirrettava_ruutu("x", x, y)
    haravasto.piirra_ruudut()


def main(kentta):
    """Lataa pelin grafiikat, luo peli-ikkunan ja asettaa siihen piirtokäsittelijän."""
    dir = os.path.dirname(os.path.abspath(__file__))
    polku = os.path.join(dir, 'spritet')
    haravasto.lataa_kuvat(polku)
    leveys = len(kentta[1]) * 40
    korkeus = len(kentta) * 40
    haravasto.luo_ikkuna(leveys, korkeus)
    haravasto.aseta_piirto_kasittelija(piirra_kentta)
    haravasto.aseta_hiiri_kasittelija(kasittele_hiiri)
    haravasto.aloita()


if __name__ == "__main__":
    while True:
        try:
            ajankohta = time.strftime("%d.%m.%Y %H:%M", time.localtime())
            aika_alku = time.time()

            statistiikka = {
                "aika": ajankohta,
                "kesto": aika_alku,
                "siirtojen_lkm": 0,
                "peli_tilanne": "",
                "kentan_pituus": 0,
                "kentan_korkeus": 0,
                "miinojenlkm": 0,
                "peli_paattyi": False
            }

            print("1 Aloita uusi peli\n2 Katso tilastoja\n3 Lopeta")
            valinta = int(input("Valitse kolmesta vaihtoehdosta syöttämällä numero: "))
            if valinta == 1:
                kentta = luo_kentta()
                kentta.reverse()
                main(kentta)

            elif valinta == 2:
                lue_statistiikka()

            elif valinta == 3:
                break
            else:
                raise ValueError
        except ValueError:
            print("Väärä syöte!")
        except FileNotFoundError:
            print("Ei löydy pelattuja pelejä")
