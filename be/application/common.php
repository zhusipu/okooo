<?php
// +----------------------------------------------------------------------
// | ThinkPHP [ WE CAN DO IT JUST THINK ]
// +----------------------------------------------------------------------
// | Copyright (c) 2006-2016 http://thinkphp.cn All rights reserved.
// +----------------------------------------------------------------------
// | Licensed ( http://www.apache.org/licenses/LICENSE-2.0 )
// +----------------------------------------------------------------------
// | Author: 流年 <liu21st@gmail.com>
// +----------------------------------------------------------------------

// 应用公共文件
function sfpText($value) {
    if ($value == null){
        return '';
    }
    $sfpMapping = [
        0   =>  '-',
        1   =>  '胜',
        2   =>  '平',
        3   =>  '负'
    ];
    $value = explode(',', $value);
    foreach ($value as $k => $v) {
        if (array_key_exists($v, $sfpMapping)) {
            $value[$k] = $sfpMapping[$v];
        }
    }
    return implode(',',$value);
}

function laocaisuanfa1($zhishu, $shangxiapan, $rangqiu) {
    $result = 0;
    if ($shangxiapan == $rangqiu && in_array($shangxiapan, $zhishu)) {
        $result = $shangxiapan;
    }
    if ($result == 2) {
        $result = 0;
    }
    return sfpText($result);
}


function laocaisuanfa2($zhishu, $shangxiapan) {
    $result = 0;
    if (in_array($shangxiapan, $zhishu)) {
        $result = $shangxiapan;
    }
    if ($result == 2) {
        $result = 0;
    }
    return sfpText($result);
}