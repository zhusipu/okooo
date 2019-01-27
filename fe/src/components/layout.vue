<template>
  <div>
    <mu-flex class="select-control-row">
      <mu-checkbox v-model="matchNotify" label="启用通知" />
    </mu-flex>
    <mu-alert color="success">
      上一次更新数据时间：{{ syncTime }}
    </mu-alert>
    <mu-tabs :value.sync="active1" color="secondary" text-color="rgba(0, 0, 0, .54)" inverse center @change="tabChange">
      <mu-tab value="laocai">老蔡算法</mu-tab>
      <mu-tab value="history">历史数据</mu-tab>
      <mu-tab value="probability">概率分析</mu-tab>
    </mu-tabs>
    <Modal
      v-model="modal1"
      :closable="false"
      title="提醒"
      @on-cancel="closeNotify">
      <audio ref="audio" autoplay="autoplay">
        <source :src="mp3Url" type="audio/mpeg">
      </audio>
      <p>比赛马上开始啦！！！</p>
      <template slot="footer">
        <Button type="primary" @click="closeNotify">确定</Button>
      </template>
    </Modal>
    <router-view />
  </div>
</template>
<script>
import { getSyncTime } from '@/api/okooo'
import { publicResult } from '@/utils/index'
import mp3Url from '@/assets/mp3/lingsheng.mp3'
export default {
  data() {
    return {
      active1: 'laocai',
      syncTime: null,
      modal1: false,
      mp3Url,
      matchNotify: false
    }
  },
  computed: {
    notifyList: function() {
      return this.$store.getters.notifyList
    }
  },
  watch: {
    matchNotify() {
      this.$refs['audio'].load()
      this.$refs['audio'].pause()
    }
  },
  created() {
    this._initTabs()
  },
  mounted() {
    this._getSyncTime()
    setInterval(this._getSyncTime, 10000)
  },
  methods: {
    test() {
      this.$refs['audio'].currentTime = 0
      this.$refs['audio'].play()
    },
    _initTabs() {
      this.active1 = this.$route.name
    },
    _getSyncTime() {
      getSyncTime().then(data => {
        this.syncTime = data.syncTime
        if (!this.matchNotify) {
          return
        }
        var groups = [
          ['zhishu', 'shangxiapan', 'fox'],
          ['zhishu', 'shangxiapan', 'fox1'],
          ['zhishu', 'rangqiu', 'shangxiapan', 'fox']
        ]
        var dtz = []
        for (let j = 0; j < data.list.length; j++) {
          const item = data.list[j]
          var param = {
            'zhishu': null,
            'rangqiu': null,
            'shangxiapan': null,
            'fox888': null,
            'fox1': null
          }
          if (item.laocaisuanfa !== null) {
            param.zhishu = item.laocaisuanfa.zhishu
            param.rangqiu = [item.laocaisuanfa.rangqiu.tidian]
            param.shangxiapan = [item.laocaisuanfa.shangxia.tidian]
            if (item.laocaisuanfa.fox008 !== null) {
              param.fox = [item.laocaisuanfa.fox008.zt]
            }
            param.fox1 = [item.laocaisuanfa.fox008Change.zt1]
            for (let g = 0; g < groups.length; g++) {
              const group = groups[g]

              // 判断是否符合条件,并且初始化一个唯一结果
              var formatParam = []
              var paramKey = []
              for (let e = 0; e < group.length; e++) {
                const key = group[e]
                if (param[key] === null || param[key] === undefined) {
                  break
                }
                paramKey.push(key)
                formatParam[e] = param[key]
              }
              paramKey = paramKey.join('+')
              var forecastResult = publicResult(formatParam)
              if (forecastResult !== 0) {
                dtz.push(item.id + paramKey)
              }
            }
          }
        }
        for (let j = 0; j < data.runList.length; j++) {
          const runitem = data.runList[j]
          var fox2 = runitem.laocaisuanfa.fox008Change.gc
          if (fox2.length > 0) {
            for (let jj = 0; jj < fox2.length; jj++) {
              dtz.push(runitem.id + 'gc' + fox2[jj].id)
            }
          }
        }
        if (dtz.length > 0) {
          var result = []
          for (let i = 0; i < dtz.length; i++) {
            if (!this.haveNotified(dtz[i])) {
              result.push(dtz[i])
            }
          }
          if (result.length > 0) {
            this._notify(result)
          }
        }
      })
    },
    haveNotified(key) {
      for (let i = 0; i < this.notifyList.length; i++) {
        if (key === this.notifyList[i]) {
          return true
        }
      }
      return false
    },
    _notify(data) {
      this.$store.dispatch('addNotify', data)
      this.modal1 = true
      this.$nextTick(() => {
        if (this.$refs['audio'].currentTime !== undefined) {
          this.$refs['audio'].currentTime = 0
        }
        this.$refs['audio'].play()
      })
    },
    closeNotify() {
      this.modal1 = false
      this.$refs['audio'].pause()
    },
    tabChange(value) {
      this.$router.push({
        path: '/' + value
      })
    }
  }
}
</script>
