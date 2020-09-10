

declare var egret: any;
declare var wx: any;
declare var WeixinJSBridge: any;

namespace meta {

    var inWx = false;
    var miniapp = false;
    var token:any = '';

    wx.miniProgram.getEnv(function (res:any) {
        inWx = true;

        if (res.miniprogram) {
            miniapp = true;
            var req = new egret.HttpRequest();
            req.responseType = egret.HttpResponseType.TEXT;

            req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
            req.open('/token/', 'GET');
            req.send();
            req.addEventListener(egret.Event.COMPLETE, function (e) {
                var res = JSON.parse(req.response);
                token = res.token;
            });
        } else {
            miniapp = false;
        }
    });

    export function api(name:string, params={}) {
        return new Promise((resolve, reject) => {
            var req = new egret.HttpRequest();
            req.responseType = egret.HttpResponseType.TEXT;

            req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
            req.open('/api/' + name + '/', 'POST');
            req.send(JSON.stringify(params));
            req.addEventListener(egret.Event.COMPLETE, function (e) {
                var res = JSON.parse(req.response);
                if (res.success) {
                    resolve(res.result);
                }
                else {
                    reject(res.result);
                }
            });
        });
    }

    export function wechat(readyFunction: Function) {
        api('get_js_ticket', {'current_url': window.location.href }).then((result:any) => {
            
            wx.config({
                debug: false,
                appId: result.appId,
                timestamp: result.timestamp,
                nonceStr: result.nonceStr,
                signature: result.signature,
                jsApiList : ['scanQRCode', 
                            'onMenuShareTimeline',
                            'onMenuShareAppMessage',
                            'onMenuShareQQ',
                            'onMenuShareWeibo' ]
            });
        
            wx.error(function(res) {
                console.log(res);
            });
        
            wx.ready(function() {
                readyFunction();
            });
        }).catch((e)=>{
            console.error(e);
        });
    }

    export function scan() {
        return new Promise((resolve, reject) => {
            wx.scanQRCode({
                needResult : 1,
                scanType : [ "qrCode"],
                success : (res:any) => {
                    resolve(res.resultStr);
                }
            });
        })
    }

    export function buy(product_id:number) {
        var successUrl:any = '/order/success/'+product_id+'/';

        if (miniapp) {
            wx.miniProgram.navigateTo({
                url: '/pages/pay/pay?pid='+product_id+'&success='+successUrl+'&token='+token 
            });
        }
        else {
            var req = new egret.HttpRequest();
            req.responseType = egret.HttpResponseType.TEXT;

            req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
            req.open('/order/public/account/' + product_id.toString() + '/', 'GET');
            req.send();
            req.addEventListener(egret.Event.COMPLETE, function () {
                var res = JSON.parse(req.response);
                WeixinJSBridge.invoke(
                    'getBrandWCPayRequest', res,
                    function(res:any){
                        if(res.err_msg == "get_brand_wcpay_request:ok" ){
                            window.location = successUrl;
                        }
                    }
                );
            });
        }
    }

    export function share (options) {
        if (miniapp) {
            wx.miniProgram.postMessage(options);
        }   
        else {
            wx.onMenuShareAppMessage(options);
            wx.onMenuShareTimeline(options);
            wx.onMenuShareQQ(options);
        }
    }
}
