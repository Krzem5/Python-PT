var fr;



function init(){
	fr=document.getElementsByClassName("contentFrame")[0];
}



window.onload=init;
window.onmessage=function(e){
	fr.height=parseInt(e.data)+fr.offsetTop;
	window.onmessage=function(e){
		switch (e.data[0]){
			case "a":
				var c=document.createElement("textarea");
				c.value=e.data.substring(1);
				c.setAttribute("readonly","");
				document.body.appendChild(c);
				c.select();
				document.execCommand("copy");
				document.body.removeChild(c);
				break;
			case "b":
				var a=document.createElement("a");
				n=e.data.substring(1).split(":")[0];
				a.href=e.data.substring(2+n.length);
				a.target="_black";
				a.download=n;
				document.body.appendChild(a);
				a.click();
				document.body.removeChild(a);
				break;
			case "c":
				window.open(e.data.substring(1));
				break;
		}
	};
};