#!/bin/bash
# -------------------------------------------------------------------------------
# Filename:    AutoGetHtrace.sh
# Revision:    1.1
# Date:        2017/08/25
# Author:      _IDLER_
# Email:       exFAT@foxmail.com
# Website:     http://ext4FAT.github.io
# Description: Systrace Helper, automatic test with systrace
# Notes:       
# -------------------------------------------------------------------------------
# Copyright:   2017 (c) _IDLER_
# License:     GPL
# -------------------------------------------------------------------------------
# Version 1.0
# Just catch Tencent-News systrace 
# -------------------------------------------------------------------------------


# -------------------------------------------------------------------------------
# App start activity table
# -------------------------------------------------------------------------------
_START_ACTIVITIES_=(
 "com.tencent.news/com.tencent.news.activity.SplashActivity"
 "com.tencent.mm/com.tencent.mm.ui.LauncherUI"
 "com.tencent.mobileqq/com.tencent.mobileqq.activity.PTVGuideActivity"
 "com.taobao.taobao/com.taobao.tao.welcome.Welcome"
 "com.sina.weibo/com.sina.weibo.SplashActivity"
 "com.immomo.momo/com.immomo.momo.android.activity.WelcomeActivity"
 "com.ss.android.article.news/com.ss.android.article.news.activity.SplashActivity"
 "com.baidu.tieba/com.baidu.tieba.LogoActivity"
 "com.UCMobile/com.UCMobile.main.UCMobile"
 "com.tencent.news/com.tencent.news.activity.SplashActivity"
 "com.eg.android.AlipayGphone/com.eg.android.AlipayGphone.AlipayLogin"
 "com.baidu.searchbox/com.baidu.searchbox.SplashActivity"
 "com.qzone/com.tencent.sc.activity.SplashActivity"
 "com.sdu.didi.psnger/com.didi.sdk.app.DidiLoadDexActivity"
 "com.smile.gifmaker/com.yxcorp.gifshow.HomeActivity"
 "com.sankuai.meituan/com.sankuai.meituan.activity.Welcome"
 "com.tencent.qqmusic/com.tencent.qqmusic.activity.AppStarterActivity"
 "com.netease.newsreader.activity/com.netease.nr.biz.ad.AdActivity"
 "com.kugou.android/com.kugou.android.app.splash.SplashActivity"
 "com.jingdong.app.mall/com.jingdong.app.mall.MainActivity"
 "com.hexin.plat.android/com.hexin.plat.android.AndroidLogoActivity"
 "com.qiyi.video/com.qiyi.video.WelcomeActivity"
 "com.tencent.mtt/com.tencent.mtt.SplashActivity"
 "com.youku.phone/com.youku.phone.ActivityWelcome"
 "com.tencent.qqlive/com.tencent.qqlive.ona.activity.WelcomeActivity"
 "com.android.dazhihui/com.android.dazhihui.dzh.dzh"
 "com.eastmoney.android.berlin/com.eastmoney.android.berlin.activity.MainActivity"
 "ctrip.android.view/ctrip.android.view.home.CtripSplashActivity"
 "com.Qunar/com.mqunar.splash.SplashActivity"
 "com.snda.wifilocating/com.lantern.launcher.ui.MainActivity"
 "com.ifeng.news1/com.ifeng.news3.activity.SplashActivity"
 "com.dianping.v1/com.dianping.main.guide.SplashScreenActivity"
 "com.baidu.netdisk/com.baidu.netdisk.ui.Navigate"
 "com.baidu.BaiduMap/com.baidu.baidumaps.WelcomeScreen"
 "com.tencent.karaoke/com.tencent.karaoke.module.splash.ui.SplashBaseActivity"
 "com.achievo.vipshop/com.achievo.vipshop.activity.LodingActivity"
 "com.autonavi.minimap/com.autonavi.map.activity.SplashActivity"
 "com.tmall.wireless/com.tmall.wireless.splash.TMSplashActivity"
 "com.tencent.qt.qtl/com.tencent.qt.qtl.activity.main.LauncherActivity"
 "com.happyelements.AndroidAnimal.qq/com.happyelements.hellolua.MainActivity"
 "com.guosen.android/com.guosen.android.ui.GuosenLogon"
 "com.didapinche.booking/com.didapinche.booking.home.activity.StartActivity"
 "tv.danmaku.bili/tv.danmaku.bili.ui.splash.SplashActivity"
 "im.yixin/im.yixin.activity.WelcomeActivity"
 "com.soft.blued/com.soft.blued.ui.welcome.FirstActivity"
 "com.tencent.qqpimsecure/com.tencent.server.fore.QuickLoadActivity"
 "com.mt.mtxx.mtxx/com.mt.mtxx.mtxx.TopViewActivity"
 "com.cubic.autohome/com.cubic.autohome.LogoActivity"
 "com.tencent.qqlite/com.tencent.mobileqq.activity.SplashActivity"
 "com.qihoo160.mobilesafe/com.qihoo360.mobilesafe.ui.index.AppEnterActivity"
 "com.shuqi.controller/com.shuqi.activity.SplashActivity"
 "com.chaozh.iReaderFree15/com.chaozh.iReader.ui.activity.WelcomeActivity"
 "com.taobao.qianniu/com.taobao.qianniu.ui.InitActivity"
 "gf.king.app/gf.king.app.InitWindow"
 "cn.wps.moffice_eng/cn.wps.moffice.writer.multiactivity.Writer1"
 "com.tencent.android.qqdownloader/com.tencent.assistant.activity.SplashActivity"
 "com.changba/com.changba.activity.Welcome"
 "air.tv.douyu.android/tv.douyu.view.activity.SplashActivity"
 "com.duowan.mobile/com.yy.mobile.ui.splash.SplashActivity"
 "com.xunlei.downloadprovider/com.xunlei.downloadprovider.loading.LoadingActivity"
 "com.letv.android.client/com.letv.android.client.activity.SplashActivity"
 "com.pplive.androidphone/com.pplive.androidphone.ui.FirstActivity"
 "com.tencent.androidqqmail/com.tencent.qqmail.LaucherActivity"
 "com.wuba/com.wuba.activity.launch.LaunchActivity"
 "com.tencent.peng/com.tencent.peng.RedGame"
 "com.guotai.dazhihui/com.android.dazhihui.view.screen.NewInitScreen"
 "cn.kuwo.player/cn.kuwo.player.activities.EntryActivity"
 "com.storm.smart/com.storm.smart.LogoActivity"
 "com.duowan.lolbox/com.duowan.lolbox.LolBoxStartActivity"
 "com.myzaker.ZAKER_Phone/com.myzaker.ZAKER_Phone.view.LogoActivity"
 "com.baidu.appsearch/com.baidu.appsearch.LauncherActivity"
)
# -------------------------------------------------------------------------------


function Unlock(){
	status=`adb shell dumpsys window policy|grep isStatusBarKeyguard|grep true`
	ri=0
	while [[ ${status} != '' ]]; do
		adb shell input keyevent 224 # Screen On
		sleep 1s
		# Double insurance
		adb shell input swipe 800 700 200 700 # Swipe Unlock
		adb shell input keyevent  82 # Unlock
		status=`adb shell dumpsys window policy|grep isStatusBarKeyguard|grep true`
		ri=$(( $ri + 1 ))
	done
}

function _Clean_Up(){
	Unlock
	PHONE_WIDTH=$1
	PHONE_HEIGHT=$2
	ratio_w=0.46625
	ratio_h=0.86953
	touch_w=$(echo $ratio_w*$PHONE_WIDTH|bc)
	touch_h=$(echo $ratio_h*$PHONE_HEIGHT|bc)
	# Clear Twice
	for r in $(seq 1 2); do
		adb shell input keyevent 187 # Square 
		adb shell input tap $touch_w $touch_h # Clean
		adb shell input keyevent 3   # Home
		adb shell am kill-all        # Kill Background
	done
}

function Clean_Up(){
	# Configuration Table
	_PRODUCT_LIST_=('MHA' 'ALP' 'sagit')
	_PHONE_WIDTHS_=(1080 1440 1080)
	_PHONE_HEIGHTS_=(1920 2560 1920)
	_NUM_=${#_PRODUCT_LIST_[@]}
	# Find procdut's name
	_PRODUCT_NAME=`adb shell getprop | grep "product.name"|cut -d ' ' -f 2`
	for ((i=0;i<$_NUM_;i++)); do
		echo "$_PRODUCT_NAME" | grep -q ${_PRODUCT_LIST_[i]}
		if [ $? -eq 0 ]; then  
			echo "Clean"
			_Clean_Up ${_PHONE_WIDTHS_[i]} ${_PHONE_HEIGHTS_[i]}
			break
		fi  
	done 
}

function FindStartActivity(){
	_PACKAGE_NAME_=$1
	_ACTIVITIES_NUMS_=${#_START_ACTIVITIES_[@]}
	for ((i=0;i<$_ACTIVITIES_NUMS_;i++)); do
		echo "${_START_ACTIVITIES_[i]}" | grep -q "$_PACKAGE_NAME_"
		if [ $? -eq 0 ]; then  
			echo ${_START_ACTIVITIES_[i]}
			break
		fi  
	done
}


function GetTrace(){
	# Variable
	_PACKAGE_NAME_=$1
	_STRATEGY_=$2
	_START_ACTIVITY_=$3
	_TEST_TIME_=`date +%Y-%m-%d_%H-%M-%S`
	_FILENAME_=traces/${_STRATEGY_}/[${_STRATEGY_}]-${_PACKAGE_NAME_}_${_TEST_TIME_}.html
	# Get trace
	adb shell atrace --async_start -b 8196 sched gfx view wm input am res idle load freq app  
	#py -2 systrace.py -o $_FILENAME_ -t 3 gfx input view wm am camera hal res dalvik rs sched freq idle disk mmc load sync workq memreclaim irq &
	py -2 systrace.py -o $_FILENAME_ -t 5 sched gfx view wm input am res idle load freq app &
	sleep 1s
	# Start Activity
	adb shell am start -n $_START_ACTIVITY_
	wait
}	


# TODO: Add more ads file location
function Block_Ads(){
	# Block Ads
	adb shell chmod 000 data/data/com.tencent.news/files/ad_cache
}


function Looper(){
	Block_Ads
	# Variable
	_STRATEGY_='JIT4'
	_PACKAGE_NAME_='com.tencent.news'
	_START_ACTIVITY_=`FindStartActivity $_PACKAGE_NAME_`
	_CNT_=50
	# Loop Run
	mkdir ./traces/$_STRATEGY_
	for i in `seq 1 $_CNT_`; do
		echo $i
		Clean_Up
		sleep 1s
		GetTrace $_PACKAGE_NAME_ $_STRATEGY_ $_START_ACTIVITY_
	done
}

function Main(){
	Looper 
}



Main
