function getIndex(elem) {
  let i = 0;
  index = elem;
  while (elem != null) {
    elem = elem.nextElementSibling;
    i++;
  };
  index = index.parentElement.children.length - i;
  return index;
};


document.querySelector('.fields-fill__body').oninput = function (event) {
  innerIndex = 0
  outerIndex = 0
  innerIndex = getIndex(event.target.parentElement)
  outerIndex = getIndex(event.target.parentElement.parentElement)
  //console.log(innerIndex, outerIndex, event.target.value)

  appfeed.data[outerIndex].feedback[innerIndex].text = event.target.value
  //console.log(appfeed.data[outerIndex].feedback[innerIndex].text)
}
// b = appfeed.bodyItems
// for (let i=0; i < b.length; i++) {let item = b[i]; if (b[i].className =="fields-fill__field-wrapper active") console.log(i);}
