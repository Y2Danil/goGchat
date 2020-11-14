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
    op: false
  },
  methods: {
    OP: function(){
      if(this.col_op){
        this.col_op = "+"+String(this.col_op);
        this.op = true;
      } else {
        this.op = false;
      }
    }
  }
});