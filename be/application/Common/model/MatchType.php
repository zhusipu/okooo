<?php

namespace app\Common\model;

use think\Model;

class MatchType extends Model
{
    //
    public function getNameById($id) {
        return $this->where('id','=',$id)->value('name');
    }
}
