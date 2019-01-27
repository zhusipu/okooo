<?php

namespace app\Common\model;

use think\Model;

class Fox008 extends Model
{
    //
    public function getDetailByMatch($match) {
        return $this->where('match', '=', $match)->find();
    }
}
