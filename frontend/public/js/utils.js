function traitArray(json_list) {
  let arr = new Set();
  console.log('traitArray start');
  json_list.forEach((item) => {
    arr.add(item.value)
  })
  let result = Array.from(arr);
  console.log('traitArray result:', result);
  return(result)
}

function nameArray(json) {
    let set = new Set();
    for(let item of json) {
        set.add(item.name)
    }
    let result = Array.from(set);
    return result
}

function arrayForGraph(json, user) {
    let arr = [];
    console.log('arrayForGraph start');
    console.log('json', json);
    console.log('user', user);
    for (let item of json) {
        tempObj = {};

        if(item.name == user) {
            tempObj['name'] = item.target_user;
            tempObj['avatar'] = item.target_user_avatar;
            tempObj['statusSide'] = item.statusSide;
            tempObj['value'] = item.value;
            tempObj['status'] = item.statusSide.toString();
            arr.push(tempObj);
        }
    }
    return arr
}

function arrayGraphModifier(item, user) {
  console.log('arrayGraphModifier start');
  console.log('item', item);
  console.log('user', user);
  const {name, avatar, status, statusSide, value} = item;
  if(item.name == user) {
    return(
      {'name':name,
      'avatar':avatar,
      'status':status,
      'statusSide':statusSide,
      'value':value}
    )
  }
  else {
    return(
      {'status':status,
      'statusSide':statusSide,
      'value':value}
    )
  }
}

function safezoneData(json_list, value) {
  console.log('safezoneData start');
  let arr = [];
  for (let item of json_list) {
      if (item.value == value) {
          arr.push(item.statusSide);
      }
  }
  console.log('safezoneData result', arr);
  return arr

}

function arraySum(array) {
      let itog = 0;
      for (let item of array) {
          itog+= item;
      }
      return itog
}

function safezone(safezoneData) {
  console.log('safezone start');
  console.log('data', safezoneData);
  let sum = arraySum(safezoneData);
  console.log('sum', sum);
  let median = Math.round(sum/safezoneData.length);
  var low = median - 16;
  var high = median + 16;
  if (low < 0) {
      low = 0;
  }
  if (high > 100) {
      high = 100;
  }
  console.log('safezone result:', {'low':low,'high':high, 'median': median})
  return({'low':low,'high':high, 'median': median})
}

function dataForGraph(json_list, user) {
  let result = [];
  for (let value of traitArray(json_list)) {
    dataRaw = arrayForGraph(json_list, user).filter(jso => jso.value == value);
    datas = [];
    for(let item of dataRaw) {
      datas.push(arrayGraphModifier(item, user));
    }
    // datas = dataRaw.map(arrayGraphModifier, user);
    temp = {
  		'data':datas,
  		'labelRange':value.split(' '),
  		'range':[1,99],
  	}
    result.push(temp);
  }
  return(result)
}

function dataForRange(json_list, user)  {
  let result = [];
  for (let value of traitArray(json_list)) {
    datas = arrayForGraph(json_list, user).filter(jso => jso.value == value);
    let others = 0;
    let self = 0;
    let safeData = safezoneData(json_list, value);
    let safe = safezone(safeData);
    datas.forEach((item, i) => {
      if(item.name != user) {
        others += item.statusSide;
      }
      else {
        self = item.statusSide;
      }
    });
    others = Math.round(others/(datas.length-1));
    temp = {
      'value':value,
      'self':self,
      'others':others,
      'tension':self - others,
      'low':safe.low,
      'high':safe.high,
    };
    result.push(temp);
  }
  console.log('dataForRange result:');
  return(result)
}

function arrayForFeedback(json, nameArray) {
    let arr = []
    for (let name of nameArray) {
        for (let item of json) {
            if(item.name == name) {
                arr.push({
                    'name':item.name,
                    'id':item.id,
                    'avatar': item.avatar,
                    'feedback': [
                        {
                            title: 'MEHR davon: Ich schätze deinen Beitrag zum gelingenden Zusammenspiel im Team…',
                            text: 'On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying'
                        },
                        {
                            title: 'ÄNDERN: du könntest zur psychologischen Sicherheit im Team beitragen, in dem...',
                            text: ''
                        },
                        {
                            title: 'FRAGEZEICHEN: ich wollte dich schon immer mal fragen…',
                            text: ''
                        }
                    ],
                });
                break
            }
        }
    }
    return arr
}



function nameArray(json) {
    let set = new Set();
    for(let item of json) {
        set.add(item.name)
    }
    let result = Array.from(set);
    return result
}

function cardsPainting(dataForRange, selectors) {
  console.log('cardsPainting start');
  console.log('cards data:', dataForRange, selectors);
  selectors.forEach((item, i) => {
    let low = dataForRange[i].low
    let high = dataForRange[i].high
    console.log('low-high', low, high);
    let selfInSafe = dataForRange[i].self>low && dataForRange[i].self<high;
    let othersInSafe = dataForRange[i].others>low && dataForRange[i].others<high;
    if (selfInSafe && othersInSafe) {item.classList.add('white__card');}
    if (selfInSafe && !othersInSafe) { item.classList.add('yellow__card');}
    if (!selfInSafe && othersInSafe) { item.classList.add('red__card');}
    if (!selfInSafe && !othersInSafe) { item.classList.add('black__card');}
  });
}