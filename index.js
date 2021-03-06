const puppeteer = require('puppeteer');

const fs = require('fs');

(async () => {
  const pageurl = 'https://kantan.vn//grammar-{index}.htm'

  const sleepFunction =　async function sleep(t) {
    return await new Promise(r => {
      setTimeout(() => {
        r();
      }, t);
    });
  }

  var crawlUrl
  var grammars = []
  for (let index = 399; index < 405; index++) {

    const browser = await puppeteer.launch({headless: false});
    const page = await browser.newPage();
    
    crawlUrl = pageurl.replace('{index}', index)
    await page.goto(crawlUrl)

    page.waitForSelector('div.GrammarDetail')

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

      let grammar = {
        level: '',
        grammarText: '',
        shortMeanText: '',
        usingMethod: '',
        detailExplain: '',
        examples: [],
        url: window.location.href
      }

      let popupElements = document.getElementsByClassName('dekiru-popup-detail')
      if(popupElements.length == 0) {
        return grammar
      }
      let popupElement = popupElements[0]

      if (popupElement == null) {
        return grammar
      }
  
      // title 
      const gmwWrap = popupElement.querySelector('div.gmw-wrap')

      if (gmwWrap == null) {
        return grammar
      }
  
      let grammarText = getContentFromChild(gmwWrap, 'p.gram')
  
      let meanText =　getContentFromChild(gmwWrap, 'p.mean')
  
      let usingMethod = getContentFromChild(popupElement, 'div.wpgam-det')
  
      let detailExplain = getContentFromChild(popupElement, 'div.grd-div')
  
      let examplesElement = popupElement.querySelector('ul.grd-ul')

      if (examplesElement == null) {
        return grammar
      }
  
      let examples = getExamples(examplesElement, 'li')
  
      let level = getContentFromChild(popupElement, 'div.swiper-wrapper > div.related-grammar-item > div.kj-n > span.level')
  
      grammar['level'] = level

      grammar['grammarText'] = grammarText

      grammar['shortMeanText'] = meanText

      grammar['usingMethod'] = usingMethod

      grammar['detailExplain'] = detailExplain

      grammar['examples'] = examples
      
      return grammar
    })

    let result = JSON.stringify(getData, null, 2)

    grammars.push(result)

    await sleepFunction(5000);

    await browser.close();
  }

  // console.log('result', grammars)

  // fs.writeFile("grammars.json", JSON.stringify(grammars), function(err) {
  //   if (err) throw err;
  //   console.log('completed')
  // })

  fs.readFile('grammars.json', function (err, data) {
    var json = JSON.parse(data)
    json = json.concat(grammars)
    fs.writeFile("grammars.json", JSON.stringify(json), function(err) {
      if (err) throw err;
      console.log('completed')
    })
  })

})();