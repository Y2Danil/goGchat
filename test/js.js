function smoke(){
  let all_message = document.getElementsByClassName('mes');
  let all_text = document.querySelector(".text");
  let m = all_text.innerHTML;
  alert("-- " + m)

  let re = /\| .* \|/g;
  let a = re.exec(m);
  alert(a);
  let d = a;
  alert(a);
  let c = a.toString().replace(/\|/g, '');
  let b = a.toString().replace(re, `<button class='smok'>${c}</button>
                                    <style>
                                      .smok {
                                        background: #000;
                                        background-blend-mode: overplay; 
                                        padding: 0;
                                        border: 0;
                                      }
                                      .smok:hover {
                                        color: #fff; 
                                        outline: 0;
                                      }
                                      .smok:focus {
                                        color: #fff; 
                                        outline: 0;
                                      }
                                    </style>`);
  alert(b);
  all_text.innerHTML = b;
  } smoke()
// 
// if(text != null){
//   for(let m in all_text.innerHTML){
//     alert(m);
//     m.style.color = 'red';
//   }
// }
