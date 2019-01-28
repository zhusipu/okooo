<template>
  <div>
    <mu-paper :z-depth="1">
      <mu-data-table :loading="loading" :columns="columns" :data="list" border>
        <template slot-scope="scope">
          <td class="is-center">
            {{ scope.row.matchType }}<br>
            {{ scope.row.name }}
          </td>
          <td class="is-center">
            {{ scope.row.matchTime }}<br>
            {{ scope.row.homeTeam }} VS {{ scope.row.visitingTeam }}<br>
            <template v-if="scope.row.laocaisuanfa !== null">
              <span v-if="scope.row.laocaisuanfa.rangqiu.value > 0">+</span> {{ scope.row.laocaisuanfa.rangqiu.value }}
              （{{ scope.row.homeTeamFen }} - {{ scope.row.visitingTeamFen }}）
            </template>
          </td>
          <template v-if="scope.row.laocaisuanfa !== null && scope.row.laocaisuanfa.fox008 !== null">
            <td class="is-center">{{ sfpText(scope.row.laocaisuanfa.zhishu) }}</td>
            <td class="is-center">
              {{ sfpText(scope.row.laocaisuanfa.rangqiu.tidian) }}<br>
              {{ scope.row.laocaisuanfa.rangqiu.avg[1].toFixed(2) }} | {{ scope.row.laocaisuanfa.rangqiu.avg[2].toFixed(2) }} | {{ scope.row.laocaisuanfa.rangqiu.avg[3].toFixed(2) }}
            </td>
            <td class="is-center">
              {{ sfpText(scope.row.laocaisuanfa.shangxia.tidian) }}<br>
              {{ scope.row.laocaisuanfa.shangxia.avg[1].toFixed(2) }} | {{ scope.row.laocaisuanfa.shangxia.avg[2].toFixed(2) }} | {{ scope.row.laocaisuanfa.shangxia.avg[3].toFixed(2) }}
            </td>
            <td class="is-center">
              {{ sfpText(scope.row.laocaisuanfa.shangxia.tidian) }}<br>
              {{ scope.row.laocaisuanfa.shangxiacompany.avg[1].toFixed(3) }} | {{ scope.row.laocaisuanfa.shangxiacompany.avg[2].toFixed(3) }} | {{ scope.row.laocaisuanfa.shangxiacompany.avg[3].toFixed(3) }}
            </td>
            <td class="is-center">
              {{ sfpText(scope.row.laocaisuanfa.peilv.tidian) }}<br>
              {{ scope.row.laocaisuanfa.peilv.avg[1].toFixed(3) }} | {{ scope.row.laocaisuanfa.peilv.avg[2].toFixed(3) }} | {{ scope.row.laocaisuanfa.peilv.avg[3].toFixed(3) }}
            </td>
            <template v-if="scope.row.laocaisuanfa.fox008 !== null">
              <td class="is-center">
                <Poptip trigger="hover" title="变化" placement="bottom" @on-popper-show="_getFox008Change(scope.row.laocaisuanfa.fox008.id)">
                  {{ sfpText(scope.row.laocaisuanfa.fox008.zt) }}
                  <template v-if="fox008List.length > 0" slot="content">
                    <mu-data-table :columns="fox008Columns" :data="fox008List">
                      <template slot-scope="scope">
                        <td class="is-center">{{ scope.row.time }}</td>
                        <td class="is-center">{{ sfpText(scope.row.zt) }}</td>
                      </template>
                    </mu-data-table>
                  </template>
                </Poptip>
                <br>
                <mu-badge :content="scope.row.laocaisuanfa.fox008.pk + ' | ' + scope.row.laocaisuanfa.fox008.gl + '%'" color="primary"/><br>
              </td>
              <td class="is-center">
                -1min：{{ sfpText(scope.row.laocaisuanfa.fox008Change.zt1) }}<br>
                <template v-if="scope.row.laocaisuanfa.fox008Change.gc.length">
                  <template v-for="(item, index) in scope.row.laocaisuanfa.fox008Change.gc">
                    <div :key="index">{{ parseInt(((new Date(item.time.replace(/\-/g, "/"))).getTime() - (new Date(scope.row.matchTime.replace(/\-/g, "/"))).getTime()) / 60000) }}min：{{ sfpText(item.zt) }}</div>
                  </template>
                </template>
              </td>
            </template>
            <template v-else>
              <td class="is-center">-</td>
              <td class="is-center">-</td>
            </template>
            <td :style="resultStyle(laocaisuanfa1(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, scope.row.laocaisuanfa.fox008.zt), rangqiuResult(scope.row.laocaisuanfa.fox008.pk, scope.row.homeTeamFen, scope.row.visitingTeamFen, 2))" class="is-center">{{ sfpText(laocaisuanfa1(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, scope.row.laocaisuanfa.fox008.zt)) }}</td>
            <td :style="resultStyle(laocaisuanfa1(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, scope.row.laocaisuanfa.fox008Change.zt1), rangqiuResult(scope.row.laocaisuanfa.fox008.pk, scope.row.homeTeamFen, scope.row.visitingTeamFen, 2))" class="is-center">{{ sfpText(laocaisuanfa1(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, scope.row.laocaisuanfa.fox008Change.zt1)) }}</td>

            <td class="is-center">
              <template v-for="(item, index) in scope.row.laocaisuanfa.fox008Change.gc">
                <div :key="index">
                  {{ parseInt(((new Date(item.time.replace(/\-/g, "/"))).getTime() - (new Date(scope.row.matchTime.replace(/\-/g, "/"))).getTime()) / 60000) }}min：{{ sfpText(laocaisuanfa1(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, item.zt)) }}
                </div>
              </template>
            </td>

            <td :style="resultStyle(laocaisuanfa2(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.rangqiu.tidian, scope.row.laocaisuanfa.fox008.zt), rangqiuResult(scope.row.laocaisuanfa.fox008.pk, scope.row.homeTeamFen, scope.row.visitingTeamFen, 2))" class="is-center" >{{ sfpText(laocaisuanfa2(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.rangqiu.tidian, scope.row.laocaisuanfa.fox008.zt)) }}</td>
            <td :style="resultStyle(laocaisuanfa3(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, scope.row.laocaisuanfa.rangqiu.tidian, scope.row.laocaisuanfa.fox008.zt), rangqiuResult(scope.row.laocaisuanfa.fox008.pk, scope.row.homeTeamFen, scope.row.visitingTeamFen, 2))" class="is-center" >{{ sfpText(laocaisuanfa3(scope.row.laocaisuanfa.zhishu, scope.row.laocaisuanfa.shangxia.tidian, scope.row.laocaisuanfa.rangqiu.tidian, scope.row.laocaisuanfa.fox008.zt)) }}</td>
          </template>
          <template v-else>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
            <td class="is-center">X</td>
          </template>
          <td class="is-center"><template v-if="scope.row.laocaisuanfa !== null && scope.row.laocaisuanfa.fox008 !== null" class="is-center">{{ sfpText(rangqiuResult(scope.row.laocaisuanfa.fox008.pk, scope.row.homeTeamFen, scope.row.visitingTeamFen, 2)) }}</template></td>
        </template>
      </mu-data-table>
    </mu-paper>
    <mu-flex justify-content="center" style="margin: 32px 0;">
      <mu-pagination :total="total" :current.sync="current" raised @change="_getLaocaiHistoryList"/>
    </mu-flex>
  </div>
</template>

<script>
import { sfpText, laocaisuanfa1, laocaisuanfa2, laocaisuanfa3, rangqiuSaiguo, fenIsSuccess, resultStyle, rangqiuResult } from '@/utils/index'
import { getLaocaiHistoryList, getFox008Change } from '@/api/okooo'
export default {
  name: 'Laocaituijian',
  data() {
    return {
      current: 1,
      total: 0,
      sfpText,
      rangqiuResult,
      resultStyle,
      fenIsSuccess,
      rangqiuSaiguo,
      laocaisuanfa1,
      laocaisuanfa2,
      laocaisuanfa3,
      loading: true,
      activeName: 'laocai',
      columns: [
        { title: '序号', width: 100, name: 'name', align: 'center' },
        { title: 'VS', name: 'vs', width: 250, align: 'center' },
        { title: '指数', name: 'zhishu', width: 80, align: 'center' },
        { title: '让球', name: 'rangqiu', align: 'center' },
        { title: '上下盘', name: 'shangxia', align: 'center' },
        { title: '上下盘公司', name: 'shangxiacompany', align: 'center' },
        { title: '凯利', name: 'kailv', align: 'center' },
        { title: 'fox', name: 'fox', align: 'center' },
        { title: 'fox1', name: 'fox1', align: 'center' },
        { title: 'Z-S-F', tooltip: '指数+上下盘+Fox008', name: 'laicaisuanfa1', align: 'center' },
        { title: 'Z-S-(F-1)', tooltip: '指数+上下盘+Fox008赛前1分钟', name: 'laicaisuanfa2', align: 'center' },
        { title: 'Z-S-FING', tooltip: '指数+上下盘+Fox008比赛中', name: 'laicaisuanfa3', align: 'center' },
        { title: 'Z-R-F', tooltip: '指数+让球+Fox008比赛中', name: 'laicaisuanfa4', align: 'center' },
        { title: 'Z-R-S-F', tooltip: '指数+让球+上下盘+FOX', name: 'laicaisuanfa5', align: 'center' },
        { title: '结果', name: 'rqsaiguo', align: 'center' }
      ],
      list: [],
      fox008Columns: [
        { title: '时间', width: 180, name: 'time', align: 'center' },
        { title: '值', width: 80, name: 'zt', align: 'center' }
      ],
      fox008List: []
    }
  },
  created() {
    this._getLaocaiHistoryList()
  },
  methods: {
    _getFox008Change(id) {
      getFox008Change(id).then(data => {
        this.fox008List = data
      })
    },
    _getLaocaiHistoryList() {
      this.loading = true
      getLaocaiHistoryList(this.current, 15).then(data => {
        this.list = data.data
        this.total = data.total
        this.loading = false
      })
    }
  }
}
</script>
