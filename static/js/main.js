

// new Vue({
//   el: '#body',
//   delimiters: ["[[", "]]"],
//   data: {
//     col_op: null,
//     op: false,
//     //ava_url: 'avatar/default_ava.jpg',
//     ava_all: null,
//     ava_new: null,
//     min_op: null,
//     only_read: false, 
//     theme_title: null,
//     el: document.getElementById("navbarBrand"),
//     revers_css: false,
//     css_span1: 'color: red;',
//     css_span2: 'color: white;'
//   },
//   methods: {
//     clickRede: function (){
//       alert('TYTYTYE');
//     },
//     OP: function(){
//       if(this.col_op){
//         this.col_op = "+"+String(this.col_op);
//         this.op = true;
//       } else {
//         this.op = false;
//       }
//     },
//     clickIMG: function(event){
//       this.ava_new = event;
//       alert(this.ava_new);
//     },
//     CkeckBox: function(){
//       this.only_read = !this.only_read;
//     },
//     Brand: function (event) {
//       let govno = this.el.querySelector('span.govno');
//       let chat = this.el.querySelector('span.chat');
//       this.revers_css = !this.revers_css;
//       if(this.revers_css){
//         this.css_span1 = 'color: white;';
//         this.css_span2 = 'color: red;';
//       } else {
//         this.css_span1 = 'color: red;';
//         this.css_span2 = 'color: white;';
//       }
//     },
//     RedirectBase: function (event) {
//       location.href = '/';
//     }
//   },
// });

new Vue({
  el: '#navbarBrand',
  data: {
    el: document.getElementById("navbarBrand"),
    revers_css: false,
    css_span1: 'color: red;',
    css_span2: 'color: white;'
  },
  methods: {
    Brand: function (event) {
      let govno = this.el.querySelector('span.govno');
      let chat = this.el.querySelector('span.chat');
      this.revers_css = !this.revers_css;
      if(this.revers_css){
        this.css_span1 = 'color: white;';
        this.css_span2 = 'color: red;';
      } else {
        this.css_span1 = 'color: red;';
        this.css_span2 = 'color: white;';
      }
    },
    RedirectBase: function (event) {
      location.href = '/';
    }
  }
});

new Vue({
  el: '#userInfo',
  delimiters: ["[[", "]]"],
  data: {
    col_op: null,
    op: false,
    ava_url: 'avatar/default_ava.jpg',
    ava_all: null,
    ava_new: null
  },
  methods: {
    OP: function(){
      if(this.col_op){
        this.col_op = "+"+String(this.col_op);
        this.op = true;
      } else {
        this.op = false;
      }
    },
    clickIMG: function(event){
      this.ava_new = event;
      alert(this.ava_new);
    }
  }
});

new Vue({
  el: '#addRubric',
  delimiters: ["[[", "]]"],
  data: {
    min_op: null,
    only_read: false, 
    theme_title: null
  },
  methods: {
    CkeckBox: function(){
      this.only_read = !this.only_read;
    }
  }
});

new Vue({
  el: '#new_avatar',
  delimiters: ["[[", "]]"],
  data: {
    ava_all: null,
    ava_new: null
  },
  methods: {
    
  }
});

// new Vue({
//   el: '#keyOpen',
//   data: {
//     key: null
//   },
//   methods: {
//     CheckKey: function(){
//       if(this.key.length != 8){
//         this.key = 'keyidiot'
//       }else{
//         // pass
//       }
//     }
//   }
// })

// new Vue({
//   el: '.pod_messag',
//   delimiters: ["[[", "]]"],
//   data: {
//     col_op: null
//   }
// });