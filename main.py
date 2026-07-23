import mwparserfromhell
import xml.etree.ElementTree as ET



def main():
    root = ET.parse('small.xml').getroot()
    for child in root:
        article_title = child[0].text
        article_text = ""
        for a in child:
            if a.tag == '{http://www.mediawiki.org/xml/export-0.11/}revision':
                for b in a:
                    if b.tag == '{http://www.mediawiki.org/xml/export-0.11/}text':
                        article_text = b.text

        wikicode = mwparserfromhell.parse(article_text)
        links = wikicode.filter_wikilinks()
        print(links)






if __name__ == "__main__":
    main()