window.onload=function(){
	function set_fold(e){
		for (var c of e.children){
			if (c.classList.contains("a")){
				c.l=e.children;
				c.addEventListener("click",function(){
					var p=this.getAttribute("data-path");
					var g;
					for (var c of this.l){
						if (c.getAttribute("data-path")==p){
							c.classList.toggle("s");
							if (c.classList.contains("go")){
								g=c;
							}
						}
					}
					function f(i=0){
						if (i>=200){
							return;
						}
						i++;
						setTimeout(f,0,i);
						var el=g;
						var gr=el.getBoundingClientRect(),gcr=el.children[0].getBoundingClientRect();
						el.style.height=(gcr.height-(gr.y-gcr.y)).toString()+"px";
						while ((el=el.parentNode.parentNode)!=null&&el.classList.contains("go")){
							gr=el.getBoundingClientRect(),gcr=el.children[0].getBoundingClientRect();
							el.style.height=(gcr.height-(gr.y-gcr.y)).toString()+"px";
						}
					}
					setTimeout(f,0);
				});
			}
			if (c.classList.contains("go")){
				c.style.height=c.children[0].offsetHeight.toString()+"px";
				c.children[0].style.width=c.offsetWidth.toString()+"px";
				c.children[0].classList.add("r");
				set_fold(c.children[0]);
			}
		}
	}
	parent.postMessage(document.body.scrollHeight,"*");
	for (var di of document.getElementsByClassName("cicon")){
		di.addEventListener("click",function(){
			var s=""
			for (var l of this.parentNode.querySelectorAll("table.table tr.l td.lc pre.code")){
				s+="\n"+l.innerText;
			}
			parent.postMessage("a"+s.substring(1),"*");
		});
	}
	for (var b of document.querySelectorAll("div.content>div.file-view>pre.view")){
		b.style.height=b.offsetHeight+"px";
		for (var c of b.children){
			if (c.classList.contains("go")){
				c.style.height=c.children[0].offsetHeight.toString()+"px";
				c.children[0].style.width=c.offsetWidth.toString()+"px";
				c.children[0].classList.add("r");
				set_fold(c.children[0]);
			}
		}
	}
	for (var cb of document.querySelectorAll("div.code-box>table.table")){
		var ll=cb.querySelectorAll("tr.l>td.ln");
		var l=ll[ll.length-1];
		var t=document.createElement("a");
		var s=getComputedStyle(l);
		t.style.fontFamily=s.fontFamily;
		t.style.fontSize=s.fontSize;
		t.innerText=l.innerText;
		document.body.appendChild(t);
		for (var k of ll){
			k.style.width=t.offsetWidth.toString()+"px";
		}
		document.body.removeChild(t);
	}
	for (var lnk of document.querySelectorAll("p.text>a.lnk")){
		lnk.addEventListener("click",function(){
			parent.postMessage("c"+this.getAttribute("l"),"*");
		})
	}
	document.getElementsByClassName("zicon")[0].addEventListener("click",function(){
		parent.postMessage("bproject.zip:"+window._download,"*");
	})
};