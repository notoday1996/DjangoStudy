(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-1471c3dc"],{"053b":function(t,a,e){"use strict";e.r(a);var s=function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"container"},[e("div",{staticClass:"left-container"},[t._m(0),e("table",{attrs:{border:"0"}},[e("tr",[e("td",[t._v("火花空间成立时间")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.spark_start_time))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("前身")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.previous_spark))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("成立至今已收集数据")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.data_nums))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("共服务学生")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.serve_student))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("目前平台共有页面")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.all_page))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("其中收录教程wiki")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.all_wiki))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("收录项目")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.all_project))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("收录问答数")]),e("td",{staticStyle:{"margin-left":"25px"}},[t._v(t._s(t.baseData.all_aq))])]),e("tr",{staticStyle:{"margin-top":"20px"}},[e("td",[t._v("更新版本")]),e("td",{staticStyle:{"margin-left":"10px"}},[t._v(t._s(t.baseData.update_times))])])])]),e("div",{staticClass:"right-container"},[e("div",{staticClass:"chartTitle"},[e("span",{staticStyle:{"font-size":"25px"}},[t._v("总体问答行为统计")]),e("span",{staticClass:"tt",staticStyle:{"margin-right":"175px"}},[t._v("总提问："+t._s(t.qaDate.total_question))]),e("span",{staticClass:"tt",staticStyle:{"margin-right":"75px"}},[t._v("总回答："+t._s(t.qaDate.total_answer))])]),e("table",{staticStyle:{"padding-left":"50px"},attrs:{border:"0"}},[e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[0]}},[t._v("1."+t._s(t.qaDate.hot_qa[0]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[1]}},[t._v("2."+t._s(t.qaDate.hot_qa[1]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[2]}},[t._v("3."+t._s(t.qaDate.hot_qa[2]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[3]}},[t._v("4."+t._s(t.qaDate.hot_qa[3]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[4]}},[t._v("5."+t._s(t.qaDate.hot_qa[4]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[5]}},[t._v("6."+t._s(t.qaDate.hot_qa[5]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[6]}},[t._v("7."+t._s(t.qaDate.hot_qa[6]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[7]}},[t._v("8."+t._s(t.qaDate.hot_qa[7]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[8]}},[t._v("9."+t._s(t.qaDate.hot_qa[8]))])])]),e("tr",[e("td",[e("a",{attrs:{href:t.qaDate.url[9]}},[t._v("10."+t._s(t.qaDate.hot_qa[9]))])])])])])])},i=[function(){var t=this,a=t.$createElement,e=t._self._c||a;return e("div",{staticClass:"title"},[e("span",{staticStyle:{color:"white"}},[t._v("火花空间基本信息")])])}],r=e("c24f"),n=(e("4328"),{name:"hello",data:function(){return{time:{startTime:"",endTime:""},qaDate:{},baseData:{}}},mounted:function(){this.handleFilter(),this.getBaseInfo(),this.drawLine()},methods:{drawLine:function(){var t=this.$echarts.init(document.getElementById("myChart"));t.setOption({tooltip:{},xAxis:{data:this.browseDate.post_title},yAxis:{},series:[{name:"文章标题",type:"bar",data:this.browseDate.count}]})},getBaseInfo:function(){console.log(this.$store.state.user),this.baseData=this.$store.state.user.baseData},handleFilter:function(){this.time.startTime="2019-11-20",this.time.endTime="2019-11-27",this.getQaStatic()},getQaStatic:function(){var t=this;console.log(this.$store.state.user);var a=this.$store.state.user.token;Object(r["i"])(this.time,a).then((function(a){console.log(a),t.qaDate=a.data,console.log(t.qaDate)}))}}}),l=n,_=(e("89f9"),e("2877")),o=Object(_["a"])(l,s,i,!1,null,"32291a43",null);a["default"]=o.exports},"3d77":function(t,a,e){},"89f9":function(t,a,e){"use strict";var s=e("3d77"),i=e.n(s);i.a}}]);