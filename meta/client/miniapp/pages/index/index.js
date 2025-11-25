// pages/main/page.js
const app = getApp();

Page({

  /**
   * 页面的初始数据
   */
  data: {
    url: ''
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var next_url = options ? (options.next_url || '/') : '/';
    var token = options ? (options.token || '') : '';

    var url = app.domain + next_url;
    if (token) {
      url += '?token=' + token;
    }
    this.setData({
      url: url
    });
  },

  getMessage: function (e) {
    var share = e.detail;
    console.log(share);
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function (options) {
    if (app.redirectUrl) {
      this.setData({
        url: app.domain + app.redirectUrl
      })
    }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {

  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {

  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {

  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {

  }
})