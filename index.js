const puppeteer = require('puppeteer');

const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch({headless: false});
  const page = await browser.newPage();

  await page.goto('https://kantan.vn//grammar-20.htm');

  const getData = await page.evaluate(() => {
      const getContentFromChild = (parentElement, childClassName) => {
      let childElement = parentElement.querySelector(childClassName)
      if (childElement != null) {
        return childElement.innerText.trim()
      } else {
        return ''
      }
    }

    const getExamples = (parentElement, childClass) => {
      var examples = []
      var exampleElements = parentElement.querySelectorAll(childClass)
      exampleElements.forEach(element => {
        var japanesesText = getContentFromChild(element, 'span.grammar-ex-japan')
        var vietnameseText = getContentFromChild(element, 'p')
        if ((japanesesText !== '') && (vietnameseText !== '')) {
            examples.push({
              japanese: japanesesText,
              vietnamese: vietnameseText
            })
        }
      })
      return examples
    }
    let popupElements = document.getElementsByClassName('dekiru-popup-detail')
    if(popupElements.length == 0) {
      return
    }
    let popupElement = popupElements[0]

    // title 
    const gmwWrap = popupElement.querySelector('div.gmw-wrap')

    let grammarText = getContentFromChild(gmwWrap, 'p.gram')

    let meanText =　getContentFromChild(gmwWrap, 'p.mean')

    let usingMethod = getContentFromChild(popupElement, 'div.wpgam-det')

    let detailExplain = getContentFromChild(popupElement, 'div.grd-div')

    let examplesElement = popupElement.querySelector('ul.grd-ul')

    let examples = getExamples(examplesElement, 'li')

    let level = getContentFromChild(popupElement, 'div.swiper-wrapper > div.related-grammar-item > div.kj-n > span.level')

    let grammar = {
      level: level,
      grammarText: grammarText,
      shortMeanText: meanText,
      usingMethod: usingMethod,
      detailExplain: detailExplain,
      examples: examples,
    }

    return grammar
  })

  let result = JSON.stringify(getData, null, 2)

  fs.readFile('grammars.json', function (err, data) {
    var json = JSON.parse(data)
    json.push(result)
    fs.writeFile("grammars.json", JSON.stringify(json), function(err) {
      if (err) throw err;
      console.log('completed')
    })
  })
  await browser.close();
})();