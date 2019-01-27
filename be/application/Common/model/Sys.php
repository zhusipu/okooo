<?php

namespace app\Common\model;

use think\Model;

class Sys extends Model
{
    //
    public function getSyncTime(){
        return $this->where('id', '=', 1)->value('syncTime');
    }
}
