export function sfpText(val) {
  val = val + ''
  val = val.split(',')
  var mapping = {
    '0': '-',
    '1': '胜',
    '2': '平',
    '3': '负'
  }
  var result = []
  for (let i = 0; i < val.length; i++) {
    if (mapping.hasOwnProperty(val[i])) {
      result.push(mapping[val[i]])
    }
  }
  return result.join(',')
}

export function laocaisuanfa3(zhishu, shangxiapan, rangqiu, fox) {
  var result = 0
  if (shangxiapan === rangqiu && shangxiapan === fox && zhishu.indexOf(shangxiapan + '') !== -1) {
    result = shangxiapan
  }
  if (result === 2) {
    result = 0
  }
  return result
}

export function laocaisuanfa2(zhishu, rangqiu, fox) {
  var result = 0
  if (rangqiu === fox && zhishu.indexOf(rangqiu + '') !== -1) {
    result = rangqiu
  }
  if (result === 2) {
    result = 0
  }
  return result
}

export function laocaisuanfa1(zhishu, shangxiapan, fox) {
  var result = 0
  if (shangxiapan === fox && zhishu.indexOf(shangxiapan + '') !== -1) {
    result = shangxiapan
  }
  if (result === 2) {
    result = 0
  }
  return result
}

export function rangqiuSaiguo(homeTeamFen, visitingTeamFen, rangqiu, result) {
  if (result === 0) {
    return 0
  }
  if ((homeTeamFen + rangqiu) === visitingTeamFen) {
    return 2
  } else if ((homeTeamFen + rangqiu) > visitingTeamFen) {
    return 1
  } else {
    return 3
  }
}

export function fenIsSuccess(fen, result) {
  if (result === 2) {
    return true
  } else if (fen !== result) {
    return false
  } else {
    return true
  }
}

export function resultStyle(fen, result) {
  var color = '#000000'
  if (result === 2) {
    color = '#000000'
  } else if (result === fen) {
    color = 'green'
  } else if (result !== fen) {
    color = 'red'
  }
  return {
    color: color,
    fontWeight: 600
  }
}

/**
 * 获取真实让球赛果
 * 赛果 1 全输、2 输一半、3 不输不赢、4 赢一半、5 全赢
 * sg = 1 2 3 4 5
 * @param {*} pk
 * @param {*} homeTeamFen
 * @param {*} visitingTeamFen
 * @param {*} type 1 正常赛果值，2 只算value1
 */
export function rangqiuResult(pk, homeTeamFen, visitingTeamFen, type) {
  var sg = null
  var gz = {
    '一/球半': {
      isBan: true,
      value: -1,
      value2: -1.5
    },
    '一球': {
      isBan: false,
      value: -1,
      value2: null
    },
    '两半': {
      isBan: false,
      value: -2.5,
      value2: null
    },
    '两半/三': {
      isBan: true,
      value: -2.5,
      value2: -3
    },
    '两球': {
      isBan: false,
      value: -2,
      value2: null
    },
    '半/一': {
      isBan: true,
      value: -0.5,
      value2: -1
    },
    '半球': {
      isBan: false,
      value: -0.5,
      value2: null
    },
    '受一/球半': {
      isBan: true,
      value: 1,
      value2: 1.5
    },
    '受一球': {
      isBan: false,
      value: 1,
      value2: null
    },
    '受两/两半': {
      isBan: true,
      value: 2,
      value2: 2.5
    },
    '三/三半': {
      isBan: true,
      value: -3,
      value2: -3.5
    },
    '两/两半': {
      isBan: true,
      value: -2,
      value2: -2.5
    },
    '受半/一': {
      isBan: true,
      value: 0.5,
      value2: 1
    },
    '受半球': {
      isBan: false,
      value: 0.5,
      value2: null
    },
    '受平/半': {
      isBan: true,
      value: 0,
      value2: 0.5
    },
    '受球半': {
      isBan: false,
      value: 1.5,
      value2: null
    },
    '平/半': {
      isBan: true,
      value: -0,
      value2: -0.5
    },
    '平手': {
      isBan: false,
      value: 0,
      value2: null
    },
    '球半': {
      isBan: false,
      value: -1.5,
      value2: null
    },
    '三球': {
      isBan: false,
      value: -3,
      value2: null
    },
    '受两半/三': {
      isBan: true,
      value: 2.5,
      value2: 3
    },
    '球半/两': {
      isBan: true,
      value: -1.5,
      value2: -2
    },
    '受两球': {
      isBan: false,
      value: 2,
      value2: null
    },
    '受球半/两': {
      isBan: true,
      value: 1.5,
      value2: 2
    }
  }
  var currPk = gz[pk]
  var result1 = matchResult(homeTeamFen + currPk.value, visitingTeamFen)
  if (currPk.isBan) {
    var result2 = matchResult(homeTeamFen + currPk.value2, visitingTeamFen)
    var result = 0
    if (result1 === 1) {
      result++
    } else if (result1 === 3) {
      result--
    }
    if (result2 === 1) {
      result++
    } else if (result2 === 3) {
      result--
    }
    if (result === 2) {
      sg = 5
    }
    if (result === 1) {
      sg = 4
    }
    if (result === -1) {
      sg = 2
    }
    if (result === -2) {
      sg = 1
    }
  } else {
    sg = result1
    if (result1 === 3) {
      sg = 1
    } else if (result1 === 2) {
      sg = 3
    } else if (result1 === 1) {
      sg = 5
    }
  }
  if (type === 2) {
    if (sg === 1 || sg === 2) {
      return 3
    } else if (sg === 3) {
      return 2
    } else if (sg === 4 || sg === 5) {
      return 1
    }
  } else {
    return sg
  }
}

/**
 * 传入比分，返回结果
 * 1 胜 2 平 3 负
 * @param {*} homeTeamFen
 * @param {*} visitingTeamFen
 */
export function matchResult(homeTeamFen, visitingTeamFen) {
  if (homeTeamFen > visitingTeamFen) {
    return 1
  } else if (homeTeamFen === visitingTeamFen) {
    return 2
  } else {
    return 3
  }
}

export function publicResult(data) {
  var results = []
  var result = null
  if (data.length === 1) {
    return data[0]
  }
  for (let i = 0; i < data[0].length; i++) {
    result = data[0][i]
    var pass = false
    for (let e = 1; e < data.length; e++) {
      const item = data[e]
      var hPass = false
      for (let j = 0; j < item.length; j++) {
        if (result + '' === item[j] + '') {
          hPass = true
          break
        }
      }
      if (!hPass) {
        pass = false
        break
      }
      pass = hPass
    }
    if (pass) {
      results.push(result)
    }
  }
  if (results.length === 1) {
    return results[0]
  } else {
    return 0
  }
}
