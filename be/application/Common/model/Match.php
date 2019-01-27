<?php

namespace app\Common\model;

use think\Exception;
use think\Model;

class Match extends Model
{
    /**
     * 根据老蔡的算法给出赛果
     * @param $id
     */
    public function getLaoCaiSuanfaResult($id){
        $result = [
            'zhishu'    =>  null,
            'rangqiu'   =>null,
            'shangxia'  =>  null,
            'fox008'    =>  null,
            'fox008Change'  =>  [
                'zt1'  =>   0,
                'zt30'  =>  0,
                'gc'    =>  []
            ],
        ];
        // 获取比赛信息
        $match = $this->where('id','=', $id)->find();
        if(!$match) {
            throw new  Exception('Match Not Found');
        }
        $fox008Model = new Fox008();
        $result['fox008'] = $fox008Model->getDetailByMatch($id);
        if ($result['fox008']) {
            // 比赛时间
            $matchTime = strtotime($match['matchTime']);

            $currTime = time();
            if ($currTime + 31 * 60 > $matchTime) {
                // 如果比赛开始了
                $fox008ChangModel = new Fox008Change();
                $result['fox008Change']['zt1'] = $fox008ChangModel
                    ->where('time', '<', date("Y-m-d H:i:s", $matchTime - 60))
                    ->where('fid', '=', $result['fox008']['id'])
                    ->order('time desc')
                    ->limit(1)
                    ->value('zt');

                // 获取比赛过程中的数据
                $result['fox008Change']['gc'] = $fox008ChangModel
                    ->whereBetween('time', [$match['matchTime'],date("Y-m-d H:i:s", $matchTime + 150 * 60)])
                    ->where('fid', '=', $result['fox008']['id'])
                    ->order('time asc')
                    ->select();

                if (!$result['fox008Change']['zt1']) {
                    $result['fox008Change']['zt1'] = $result['fox008']['zt'];
                }
            }
        }
        // 获取指数提点结果
        $zhishuModel = new Zhishu();

        $zhishuInfo = $zhishuModel->where('match', '=', $id)->find();
        if (!$zhishuInfo) {
            throw new  Exception('Zhishu Not Found');
        }
        $tidian = explode(',', $zhishuInfo['remind']);
        $result['zhishu'] = $tidian;

        // 获取让球均值
        $rangqiuModel = new Rangqiu();
        $rangqiuList = $rangqiuModel->where('match', '=', $id)->limit(8)->select();
        if (!$rangqiuList || count($rangqiuList) == 0) {
            throw new  Exception($id.'Ranggqiu Data Not Found');
        }
        $result['rangqiu']['value'] = $rangqiuList[0]['rangqiu'];
        $mapping = [1,2,3];

        $rangqiuResultList = [];
        foreach($mapping as $v) {
            $field = '';
            switch ($v) {
                case 1:
                    $field = 'newzhushengzhishu';
                    break;
                case 2;
                    $field = 'newpingjuzhishu';
                    break;
                case 3;
                    $field = 'newkeshengzhishu';
                    break;
            }
            $sum = 0;
            foreach ($rangqiuList as $item) {
                $sum += $item[$field];
            }
            $value = $sum / count($rangqiuList);
            $rangqiuResultList[$v] = $value;
        }
        $value = null;
        $rangqiuTidian = null;
        foreach($rangqiuResultList as $jg => $v) {
            $result['rangqiu']['avg'][$jg] = $v;
            if ($v < $value || $value == null) {
                $value = $v;
                $rangqiuTidian = $jg;
            }
        }
        $result['rangqiu']['tidian'] = $rangqiuTidian;


        $inCompany = [
            'Bet365', '威廉.希尔','立博','bwin','澳门彩票','伟德国际','必发'
        ];
        $companyModel = new Company();
        $inCompanyIds = $companyModel->whereIn('name', $inCompany)->column('id');
        // 获取上下均值
        $shangxiaModel = new Shangxia();
        $shangxiaList = $shangxiaModel->where('match', '=', $id)->select();
        if (!$shangxiaList|| count($shangxiaList) == 0) {
            throw new  Exception('Shangxia Data Not Found');
        }
        $shangxiaResultList = [];
        $min = [
            'newshanghui'   =>  null,
            'newpankou'   =>  null,
            'newxiashui'   =>  null
        ];
        $max = [
            'newshanghui'   =>  null,
            'newpankou'   =>  null,
            'newxiashui'   =>  null
        ];
        foreach($mapping as $v) {
            $field = '';
            switch ($v) {
                case 1:
                    $field = 'newshanghui';
                    break;
                case 2;
                    $field = 'newpankou';
                    break;
                case 3;
                    $field = 'newxiashui';
                    break;
            }
            $sum = 0;
            $companySum = 0;
            $companyCount = 0;
            foreach ($shangxiaList as $item) {
                $sum += $item[$field];
                if (in_array($item['company'], $inCompanyIds)) {
                    $companyCount++;
                    if ($min[$field] == null) {
                        $min[$field] = $item[$field];
                    } else if ($min[$field] > $item[$field]) {
                        $min[$field] = $item[$field];
                    }
                    if ($max[$field] == null) {
                        $max[$field] = $item[$field];
                    } else if ($max[$field] < $item[$field]) {
                        $max[$field] = $item[$field];
                    }
                    $companySum += $item[$field];
                }
            }
            $count = count($shangxiaList);
            if ($companyCount > 3) {
                $companySum = $companySum - $max[$field] - $min[$field];
                $companyCount = $companyCount - 2;
            }
            $shangxiaResultList[$v][0] = $sum / $count;
            $shangxiaResultList[$v][1] = $companySum / $companyCount;
        }
        $value0 = null;
        $value1 = null;
        $shangxiaTidian = null;
        foreach($shangxiaResultList as $jg => $v) {
            $result['shangxia']['avg'][$jg] = $v[0];
            $result['shangxiacompany']['avg'][$jg] = $v[1];
            if ($v[0] < $value0 || $value0 == null) {
                $value0 = $v[0];
                $shangxiaTidian = $jg;
                $result['shangxia']['tidian'] = $shangxiaTidian;
            }
            if ($v[1] < $value1 || $value1 == null) {
                $value0 = $v[1];
                $shangxiaTidian = $jg;
                $result['shangxiacompany']['tidian'] = $shangxiaTidian;
            }
        }
        return $result;
    }

    /**
     * 获取临近的比赛
     * @param int $page
     * @param int $listRows
     * @return \think\db\Query
     */
    public function getLinJinMatchList($page = 1, $listRows = 10){
        $currDate = date("Y-m-d H:i:s", time() - 2 * 60 * 60);
        $endCurrDate = date("Y-m-d H:i:s", strtotime(date("Y-m-d 00:00:01", time() + 4 * 24 * 60 * 60)) + 1);
        return $this
            ->whereBetween('matchTime',[$currDate,$endCurrDate])
            ->order('matchTime')
            ->page($page, $listRows)
            ->select();
    }

    public function getHistoryMatchList($page = 1, $listRows = 10){
        $currDate = date("Y-m-d H:i:s", time());
        $data = $this
            ->where('matchTime', '<', $currDate)
            ->order('matchTime desc')
            ->page($page, $listRows)
            ->select();
        $total = $this
            ->where('matchTime', '<', $currDate)
            ->order('matchTime desc')
            ->count();
        return [
            'data'  =>  $data,
            'total' =>  $total
        ];
    }

    public function getMatchListByTime($startDate, $endDate) {
        $startDate .= ' 00:00:01';
        $endDate .= ' 23:59:59';
        return $this
            ->whereBetween('matchTime',[$startDate, $endDate])
            ->order('matchTime desc')
            ->select();
    }
}
