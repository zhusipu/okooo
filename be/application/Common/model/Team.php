<?php

namespace app\Common\model;

use think\Model;

class Team extends Model
{
    //
    public function getNameById($id) {
        return $this->where('id','=',$id)->value('name');
    }
}
