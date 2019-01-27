<?php
namespace app\index\controller;

use app\Common\model\Fox008Change;
use app\Common\model\Match;
use app\Common\model\MatchType;
use app\Common\model\Sys;
use app\Common\model\Team;
use think\Controller;
use think\Exception;

class Okooo extends Controller
{

    public function getSyncTime() {
        $sysModel = new Sys();
        $matchModel = new Match();
        $currTime = date("Y-m-d H:i:s", time());
        $weilaicurrTime = date("Y-m-d H:i:s", time() + 2 * 60);
        $list = $matchModel->whereBetween('matchTime',  [$currTime, $weilaicurrTime])->select();
        $runlist = $matchModel->whereBetween('matchTime',[date("Y-m-d H:i:s",time() - 150 * 60), $currTime])->select();
        foreach ($list as $k=>$v){
            try{
                $list[$k]['laocaisuanfa'] = $matchModel->getLaoCaiSuanfaResult($v['id']);
            }catch (Exception $e) {
                $list[$k]['laocaisuanfa'] = null;
            }
        }
        foreach ($runlist as $k=>$v){
            try{
                $runlist[$k]['laocaisuanfa'] = $matchModel->getLaoCaiSuanfaResult($v['id']);
            }catch (Exception $e) {
                $runlist[$k]['laocaisuanfa'] = null;
            }
        }
        return [
            'syncTime'  =>  $sysModel->getSyncTime(),
            'list' =>  $list,
            'runList' =>  $runlist
        ];
    }

    public function getLaocaiList($page = 1, $listRows = 100)
    {
        // 获取现在的时间
        $matchModel = new Match();
        $teamModel = new Team();
        $matchTypeModel = new MatchType();
        $list = $matchModel->getLinJinMatchList($page, $listRows);
        foreach ($list as $k=>$v){
            $list[$k]['matchType'] = $matchTypeModel->getNameById($v['matchType']);
            $list[$k]['homeTeam'] = $teamModel->getNameById($v['homeTeam']);
            $list[$k]['visitingTeam'] = $teamModel->getNameById($v['visitingTeam']);
            try{
                $list[$k]['laocaisuanfa'] = $matchModel->getLaoCaiSuanfaResult($v['id']);
            }catch (Exception $e) {
                $list[$k]['laocaisuanfa'] = null;
            }
        }
        return $list;
    }
    public function getLaocaiHistoryList($page = 1, $listRows = 50)
    {
        // 获取现在的时间
        $matchModel = new Match();
        $teamModel = new Team();
        $matchTypeModel = new MatchType();
        $data = $matchModel->getHistoryMatchList($page, $listRows);
        foreach ($data['data'] as $k=>$v){
            $data['data'][$k]['matchType'] = $matchTypeModel->getNameById($v['matchType']);
            $data['data'][$k]['homeTeam'] = $teamModel->getNameById($v['homeTeam']);
            $data['data'][$k]['visitingTeam'] = $teamModel->getNameById($v['visitingTeam']);
            try{
                $data['data'][$k]['laocaisuanfa'] = $matchModel->getLaoCaiSuanfaResult($v['id']);
            }catch (Exception $e) {
                dump($e->getMessage());
                $data['data'][$k]['laocaisuanfa'] = null;
            }
        }
        return $data;
    }


    public function getProbability($startDate, $endDate) {
        // 获取近30天的概率
        $matchModel = new Match();
        $list = $matchModel->getMatchListByTime($startDate, $endDate);
        foreach ($list as $k=>$v){
            try{
                $list[$k]['laocaisuanfa'] = $matchModel->getLaoCaiSuanfaResult($v['id']);
            }catch (Exception $e) {
                $list[$k]['laocaisuanfa'] = null;
            }
        }
        return $list;
    }

    public function getFox008Change($id) {
        $fox008Change = new Fox008Change();
        return $fox008Change->where('fid', '=',$id)->limit(10)->order('id desc')->select();
    }
}
