<template>
  <mu-row gutter>
    <mu-col span="12" lg="12" sm="12">
      <mu-form ref="form" :model="form" :inline="true" label-position="left" class="mu-demo-form">
        <mu-form-item label="起始时间" prop="username">
          <mu-date-input v-model="form.startDate" type="date" value-format="YYYY-MM-DD" label-float full-width />
        </mu-form-item>
        <mu-form-item label="结束时间" prop="password">
          <mu-date-input v-model="form.endDate" type="date" value-format="YYYY-MM-DD" label-float full-width />
        </mu-form-item>
        <mu-form-item>
          <mu-button color="primary" @click="_getProbability">查询</mu-button>
        </mu-form-item>
      </mu-form>
    </mu-col>
    <mu-col span="12" lg="12" sm="12">
      <mu-form ref="form" :model="form" :inline="true" label-position="left" class="mu-demo-form">
        <mu-form-item label="盘口" prop="password">
          <mu-text-field v-model="form.pk" label-float full-width />
        </mu-form-item>
        <mu-form-item label="比分1" prop="password">
          <mu-text-field v-model="form.bifen1" label-float full-width />
        </mu-form-item>
        <mu-form-item label="比分2" prop="password">
          <mu-text-field v-model="form.bifen2" label-float full-width />
        </mu-form-item>
        <mu-form-item>
          <mu-button color="primary" @click="jisuanRangqiuResult">查询</mu-button>
        </mu-form-item>
      </mu-form>
    </mu-col>
    <mu-col span="12" lg="12" sm="12">
      <p>结果1概率{{ r1s/ r1 }} 成功了 {{ r1s }}, 符合条件的总数{{ r1 }}</p>
      <p>结果2概率{{ r2s/ r2 }} 成功了 {{ r2s }}, 符合条件的总数{{ r2 }}</p>
    </mu-col>
  </mu-row>
</template>
<script>
import { publicResult, rangqiuResult } from '@/utils/index'
import echarts from 'echarts'
import { getProbability } from '@/api/okooo'
export default {
  data() {
    return {
      form: {
        startDate: null,
        endDate: null,
        pk: null,
        bifen1: null,
        bifen2: null
      },
      data: [],
      chart: null,
      r1: 0,
      r1s: 0,
      total: 0,
      r2: 0,
      r2s: 0,
      error: 0,
      id: 'myEcharts'
    }
  },
  methods: {
    jisuanRangqiuResult() {
      console.log(rangqiuResult(this.form.pk, parseInt(this.form.bifen1), parseInt(this.form.bifen2), 2))
    },
    initChart() {
      this.chart = echarts.init(document.getElementById(this.id))
    },
    _getProbability() {
      getProbability(this.form.startDate, this.form.endDate).then(data => {
        this.data = data
        // this._jisuan(this.data)
        this._jisuan(this.data)
      })
    },
    _jisuan(data) {
      var result = {}
      var groups = [
        // ['zhishu'],
        // ['rangqiu'],
        // ['shangxiapan'],
        // ['fox'],
        ['fox1'],
        // ['zhishu', 'fox'],
        // ['zhishu', 'rangqiu', 'shangxiapan', 'fox'],
        // ['zhishu', 'rangqiu', 'shangxiapan'],
        // ['zhishu', 'rangqiu'],
        // ['zhishu', 'rangqiu', 'fox'],
        // ['zhishu', 'shangxiapan'],
        ['zhishu', 'shangxiapan', 'fox1']
        // ['rangqiu', 'shangxiapan', 'fox'],
        // ['rangqiu', 'shangxiapan'],
        // ['shangxiapan', 'fox'],
        // ['shangxiapan', 'rangqiu']
      ]
      for (let i = 0; i < data.length; i++) {
        var item = data[i]
        var param = {
          'zhishu': null,
          'rangqiu': null,
          'shangxiapan': null,
          'fox888': null,
          'fox1': null
        }
        var pk = null
        if (item.laocaisuanfa !== null) {
          param.zhishu = item.laocaisuanfa.zhishu
          param.rangqiu = [item.laocaisuanfa.rangqiu.tidian]
          param.shangxiapan = [item.laocaisuanfa.shangxia.tidian]
          if (item.laocaisuanfa.fox008 !== null) {
            param.fox = [item.laocaisuanfa.fox008.zt]
            param.fox1 = [item.laocaisuanfa.fox008Change.zt1]
            pk = item.laocaisuanfa.fox008.pk
          }
        }
        if (pk === null) {
          continue
        }
        // 组合 指数+让球+上下盘+FOX
        for (let g = 0; g < groups.length; g++) {
          const group = groups[g]

          // 判断是否符合条件,并且初始化一个唯一结果
          var join = true
          var formatParam = []
          var paramKey = []
          for (let e = 0; e < group.length; e++) {
            const key = group[e]
            if (param[key] === null || param[key] === undefined) {
              join = false
              break
            }
            paramKey.push(key)
            formatParam[e] = param[key]
          }
          paramKey = paramKey.join('+')
          if (!join) {
            continue
          }
          if (!result.hasOwnProperty(paramKey)) {
            result[paramKey] = {
              total: 0,
              success: 0,
              listPing: [],
              listSheng: []
            }
          }
          // 获取预测结果
          var saiguo = rangqiuResult(pk, item.homeTeamFen, item.visitingTeamFen, 2)
          var forecastResult = publicResult(formatParam)
          if (typeof forecastResult === 'object') {
            if (saiguo + '' === '2') {
              result[paramKey].success++
              console.log(pk, item.homeTeamFen, item.visitingTeamFen)
              result[paramKey].listPing.push(item)
              break
            }
            result[paramKey].total++
            for (let f = 0; f < forecastResult.length; f++) {
              if (forecastResult[f] + '' === saiguo + '') {
                result[paramKey].success++
                result[paramKey].listSheng.push(item)
                break
              }
            }
          } else {
            if (forecastResult !== 0) {
              result[paramKey].total++
              if (saiguo + '' === '2') {
                result[paramKey].success++
                console.log(pk, item.homeTeamFen, item.visitingTeamFen, saiguo)
                result[paramKey].listPing.push(item)
                break
              }
              // 获取比赛结果
              // 如果预测和结果相等，那么加1
              if (forecastResult + '' === saiguo + '') {
                result[paramKey].success++
                result[paramKey].listSheng.push(item)
              }
            }
          }
        }
      }
      console.log(result)
      for (var r in result) {
        console.log('组合：' + r + ',总数：' + result[r].total + ',成功数：' + result[r].success + ',概率' + (result[r].success / result[r].total))
      }
    }
  }
}
</script>
