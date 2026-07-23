import mwparserfromhell
import xml.etree.ElementTree as ET



def filter_wiki_links_r(wiki: str) -> list[str]:
    links = mwparserfromhell.parse(wiki).filter_wikilinks()
    tmp = []
    for link in links:
        l = filter_wiki_links_r(link[2:-2]) # take [[x]] -> x
        if len(l) == 0:
            tmp.append(link)
            continue

        for ele in l:
            tmp.append(ele)


    result = []
    for item in tmp:
        s = item.split("|")[0]
        if s[-2:] != "]]":
            s += "]]"
        result.append(s)

    return result

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
        if article_title == "Albedo":
            print(article_text)
            links = filter_wiki_links_r(article_text)
            print(f"{article_title}: {links}")







if __name__ == "__main__":
    main()