import request from '@/utils/request'

export function getSyncTime() {
  return request({
    url: '/okooo/getSyncTime',
    method: 'get'
  })
}

export function getLaocaiList(page, listRows) {
  return request({
    url: '/okooo/getLaocaiList',
    method: 'get',
    params: {
      page,
      listRows
    }
  })
}

export function getLaocaiHistoryList(page, listRows) {
  return request({
    url: '/okooo/getLaocaiHistoryList',
    method: 'get',
    params: {
      page,
      listRows
    }
  })
}

export function getProbability(startDate, endDate) {
  return request({
    url: '/okooo/getProbability',
    method: 'get',
    params: {
      startDate,
      endDate
    }
  })
}

export function getFox008Change(id) {
  return request({
    url: '/okooo/getFox008Change',
    method: 'get',
    params: {
      id
    }
  })
}
