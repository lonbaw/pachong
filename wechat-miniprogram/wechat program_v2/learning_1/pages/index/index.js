let app = getApp();
Page({
 data: {
  isSubmit: false,
  isExport: false,
  keyword: "",
  result:[],
  file_path:"",
 },
 DaochuSubmit: function(e){
  console.log('开始导出excel');
  let _this = this;
  let column = e.detail.value;
  console.log(column.cmp_full_name);
  wx.request({
    url: 'http://localhost:8888/export',
    method: "POST",
    data: column,
    header: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    success: (res) => {
     
      this.setData({
        isExport: true,
        file_path: res.data,
        texthref: res.data
      })
    }
  })
 },
 formSubmit: function (e) {
  console.log('form发生了submit事件，携带数据为：', e.detail.value);
  let _this = this;
  let column = e.detail.value;
  console.log(column.keyword);
  wx.request({
    url: 'http://localhost:8888',
    method: "POST",
    data: column,
    header: {
      "Content-Type": "application/x-www-form-urlencoded"
    },
    success: (res) => {
      
      this.setData({
        isSubmit: true,
        result:res.data,
      })
    }
  })},
 formReset: function () {
  console.log('form发生了reset事件')
 }
})
