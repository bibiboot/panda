var META_DICT = {};
var CAT_DICT = {};
var gi = gi || {};

var giHost = window.location.host;
var giProtocol = (document.location.protocol == "https:") ? "https://" : "http://";

function $g(keyid){ return document.getElementById(keyid); }
function $n(keyn){ return document.getElementsByName(keyn); }

gi.suggest = {
        getDummy: function(){
            var data = {"center":[-12.2686,125.568,-23.6326],"normal":[0.0901181,0.00440694,-0.995921],
 "progress":1.03339,"radius":22.953,"id":39,"handIds":[42],"pointableIds":[18],"duration":524417,"state":"stop","type":"circle"};
            this.suggVal = data;
        },
        getKeyTap: function(){
            var data = {"position":[6.25641,114.305,-15.591],"direction":[0.226298,-0.973463,-0.034035],"progress":1,"id":46,"handIds":[96],"pointableIds":[68],"duration":108158,"state":"stop","type":"keyTap" };
            this.suggVal = data;
        },
	getSearch: function(myEvent, suggVal){
	    myEvent=window.event || myEvent;
	    /*this.iKeyCode=myEvent.keyCode;*/
	    this.suggVal = suggVal;		    
             this.getKeyTap();
             //this.getDummy();
	     this.getApi();    			
	},
	getApi: function(){		
	    	this.nowElm = -1;	    	
	    	gi.ajax.get({
				url: '/homenext/?',
				params: 'center='+ this.suggVal['center'] +'&progress='+this.suggVal['progress'] + '&radius=' + this.suggVal['radius'] + '&handIds='+this.suggVal['handIds']+'&pointableIds='+this.suggVal['handIds']+'&duration='+this.suggVal['duration']+'&state='+this.suggVal['state']+'&type='+this.suggVal['type']+'&position='+this.suggVal['position']+'&songid='+$g('songid').value +'&direction='+this.suggVal['direction'],
				success: 'homeSuccess'
			});
	},
        renderResult: function(cityJson){
                console.log(cityJson);
		cityJson = eval(cityJson);

             data = ['Lady Gaga', 
            'Telephone', 
            '2001', '2003',
            'Pop', 'EMD', 'Dance',
            'Happy', 'Sad',
            'Rome', 'Italy',
            'http://akamai-b.cdn.cddbp.net/cds/2.0/image-artist/79BD/D0F7/08E9/8855_medium_front.jpg', 
            'I am good']


		if(cityJson.length==0){ this.hidePlaces(); return false; }				
                $g('artist').innerHTML = cityJson[0]
                $g('song').innerHTML = cityJson[1]
                $g('era1').innerHTML = cityJson[2]
                $g('era2').innerHTML = cityJson[3]
                $g('genre1').innerHTML = cityJson[4]
                $g('genre2').innerHTML = cityJson[5]
                $g('mood1').innerHTML = cityJson[6]
                $g('mood2').innerHTML = cityJson[7]
                $g('city1').innerHTML = cityJson[8]
                $g('city2').innerHTML = cityJson[9]
                $g('url').innerHTML = "<img src='"+cityJson[10]+"' class='poster'></img>";
                $g('about').innerHTML = cityJson[11];
                $g('songid').value = cityJson[12];
        },
	keyHandler: function(){		
	    switch(this.iKeyCode){
	       case 38: 
	          /*this.goUp();*/
	          break;
	       case 40: 
	          /*this.goDown();*/
	          break;
	       case 13:	       	  
	       	  this.hideCity();	  	       	        	  
	       	  break;
	       case 9:	       	 
	       	  this.hideCity();    
	          break;	       
	    }
 	},
 	hideCity: function(){		
	},
 	hidePlaces: function(){		
                $g('result').innerHTML = '';
	},
 	about: function(){		
		$g('aboutus').className = 'center';
	},
 	goUp: function(){
	    if(nodeCount>0 && this.nowElm>0){
	       --this.nowElm;	       
	       for(var i=0;i<nodeCount;i++){
	          if(i==this.nowElm){
	          }else{
	             this.getElm.childNodes[i].className="";
	          }
	       }
	    }
	},
	goDown: function(){
	    if(nodeCount>0 && this.nowElm<(nodeCount-1)){
	       ++this.nowElm;	      
	       for(var i=0;i<nodeCount;i++){
	          if(i==this.nowElm){
	          }else{
	          }
	       }
	    }
	},	
}

function homeSuccess(cityJson){ gi.suggest.renderResult(cityJson); }
function load(){
    data = $g('data').value;
    gi.suggest.renderResult(data);
}

gi.ajax = {
	getAjaxObject: function(){
		var goHttp = false;
		if(window.XMLHttpRequest){ goHttp = new XMLHttpRequest(); }
		else if(window.ActiveXObject){
			try{ goHttp = new ActiveXObject('Msxml2.XMLHTTP'); }
			catch(ef){ try{ goHttp = new ActiveXObject('Microsoft.XMLHTTP'); }
			catch(es){ this.getError('Please enable Javascript'); }}
		}
		return goHttp;		
	},
	getAjaxReady: function(getHttp, callSuccess){		
		return function(){
			if(getHttp.readyState == 4){
				if(getHttp.status == 200){ window[callSuccess](getHttp.responseText); giajst = 0; /*alert(getHttp.responseText);*/ }
				else{ this.getError('Sorry we are facing some issue in processing your request'); giajst = 0; }				
			}					
		}
	},
	post: function(giObj){		
		var getHttp = this.getAjaxObject();		
		getHttp.onreadystatechange = this.getAjaxReady(getHttp, giObj.success);
		getHttp.open('POST', giObj.url, true);
		getHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		getHttp.send(giObj.params);		
	},
	get: function(giObj){		
		var getHttp = this.getAjaxObject();		
		getHttp.onreadystatechange = this.getAjaxReady(getHttp, giObj.success);
		getHttp.open('GET', giObj.url+giObj.params, true);
		getHttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
		getHttp.send();		
	},
	getError : function(errMsg){
		$('gerb').className = 'db';	
		$('gerb').innerHTML = '<em>'+errMsg+'</em>';		
	},
	getSetting: function(settId){			
		if($(settId).className == 'dn'){ $(settId).className = 'db'; giOpenSett = settId;  }
		else{ $(settId).className = 'dn' }			
	},
	closeSetting: function(){			
		if(giOpenSett != ''){ $(giOpenSett).className = 'dn'; }		
	} 
};

