(function(){const w=document.createElement("link").relList;if(w&&w.supports&&w.supports("modulepreload"))return;for(const b of document.querySelectorAll('link[rel="modulepreload"]'))r(b);new MutationObserver(b=>{for(const H of b)if(H.type==="childList")for(const B of H.addedNodes)B.tagName==="LINK"&&B.rel==="modulepreload"&&r(B)}).observe(document,{childList:!0,subtree:!0});function L(b){const H={};return b.integrity&&(H.integrity=b.integrity),b.referrerPolicy&&(H.referrerPolicy=b.referrerPolicy),b.crossOrigin==="use-credentials"?H.credentials="include":b.crossOrigin==="anonymous"?H.credentials="omit":H.credentials="same-origin",H}function r(b){if(b.ep)return;b.ep=!0;const H=L(b);fetch(b.href,H)}})();var cs={exports:{}},xn={};var gd;function Ih(){if(gd)return xn;gd=1;var j=Symbol.for("react.transitional.element"),w=Symbol.for("react.fragment");function L(r,b,H){var B=null;if(H!==void 0&&(B=""+H),b.key!==void 0&&(B=""+b.key),"key"in b){H={};for(var D in b)D!=="key"&&(H[D]=b[D])}else H=b;return b=H.ref,{$$typeof:j,type:r,key:B,ref:b!==void 0?b:null,props:H}}return xn.Fragment=w,xn.jsx=L,xn.jsxs=L,xn}var yd;function ep(){return yd||(yd=1,cs.exports=Ih()),cs.exports}var c=ep(),us={exports:{}},K={};var bd;function lp(){if(bd)return K;bd=1;var j=Symbol.for("react.transitional.element"),w=Symbol.for("react.portal"),L=Symbol.for("react.fragment"),r=Symbol.for("react.strict_mode"),b=Symbol.for("react.profiler"),H=Symbol.for("react.consumer"),B=Symbol.for("react.context"),D=Symbol.for("react.forward_ref"),E=Symbol.for("react.suspense"),h=Symbol.for("react.memo"),O=Symbol.for("react.lazy"),A=Symbol.for("react.activity"),W=Symbol.iterator;function U(d){return d===null||typeof d!="object"?null:(d=W&&d[W]||d["@@iterator"],typeof d=="function"?d:null)}var se={isMounted:function(){return!1},enqueueForceUpdate:function(){},enqueueReplaceState:function(){},enqueueSetState:function(){}},_e=Object.assign,tl={};function q(d,T,C){this.props=d,this.context=T,this.refs=tl,this.updater=C||se}q.prototype.isReactComponent={},q.prototype.setState=function(d,T){if(typeof d!="object"&&typeof d!="function"&&d!=null)throw Error("takes an object of state variables to update or a function which returns an object of state variables.");this.updater.enqueueSetState(this,d,T,"setState")},q.prototype.forceUpdate=function(d){this.updater.enqueueForceUpdate(this,d,"forceUpdate")};function be(){}be.prototype=q.prototype;function ve(d,T,C){this.props=d,this.context=T,this.refs=tl,this.updater=C||se}var ke=ve.prototype=new be;ke.constructor=ve,_e(ke,q.prototype),ke.isPureReactComponent=!0;var nl=Array.isArray;function qe(){}var P={H:null,A:null,T:null,S:null},je=Object.prototype.hasOwnProperty;function $e(d,T,C){var M=C.ref;return{$$typeof:j,type:d,key:T,ref:M!==void 0?M:null,props:C}}function Ue(d,T){return $e(d.type,T,d.props)}function Ke(d){return typeof d=="object"&&d!==null&&d.$$typeof===j}function Re(d){var T={"=":"=0",":":"=2"};return"$"+d.replace(/[=:]/g,function(C){return T[C]})}var Tl=/\/+/g;function we(d,T){return typeof d=="object"&&d!==null&&d.key!=null?Re(""+d.key):T.toString(36)}function il(d){switch(d.status){case"fulfilled":return d.value;case"rejected":throw d.reason;default:switch(typeof d.status=="string"?d.then(qe,qe):(d.status="pending",d.then(function(T){d.status==="pending"&&(d.status="fulfilled",d.value=T)},function(T){d.status==="pending"&&(d.status="rejected",d.reason=T)})),d.status){case"fulfilled":return d.value;case"rejected":throw d.reason}}throw d}function N(d,T,C,M,y){var X=typeof d;(X==="undefined"||X==="boolean")&&(d=null);var J=!1;if(d===null)J=!0;else switch(X){case"bigint":case"string":case"number":J=!0;break;case"object":switch(d.$$typeof){case j:case w:J=!0;break;case O:return J=d._init,N(J(d._payload),T,C,M,y)}}if(J)return y=y(d),J=M===""?"."+we(d,0):M,nl(y)?(C="",J!=null&&(C=J.replace(Tl,"$&/")+"/"),N(y,T,C,"",function(Tt){return Tt})):y!=null&&(Ke(y)&&(y=Ue(y,C+(y.key==null||d&&d.key===y.key?"":(""+y.key).replace(Tl,"$&/")+"/")+J)),T.push(y)),1;J=0;var Ye=M===""?".":M+":";if(nl(d))for(var ze=0;ze<d.length;ze++)M=d[ze],X=Ye+we(M,ze),J+=N(M,T,C,X,y);else if(ze=U(d),typeof ze=="function")for(d=ze.call(d),ze=0;!(M=d.next()).done;)M=M.value,X=Ye+we(M,ze++),J+=N(M,T,C,X,y);else if(X==="object"){if(typeof d.then=="function")return N(il(d),T,C,M,y);throw T=String(d),Error("Objects are not valid as a React child (found: "+(T==="[object Object]"?"object with keys {"+Object.keys(d).join(", ")+"}":T)+"). If you meant to render a collection of children, use an array instead.")}return J}function R(d,T,C){if(d==null)return d;var M=[],y=0;return N(d,M,"","",function(X){return T.call(C,X,y++)}),M}function k(d){if(d._status===-1){var T=d._result;T=T(),T.then(function(C){(d._status===0||d._status===-1)&&(d._status=1,d._result=C)},function(C){(d._status===0||d._status===-1)&&(d._status=2,d._result=C)}),d._status===-1&&(d._status=0,d._result=T)}if(d._status===1)return d._result.default;throw d._result}var ue=typeof reportError=="function"?reportError:function(d){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var T=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof d=="object"&&d!==null&&typeof d.message=="string"?String(d.message):String(d),error:d});if(!window.dispatchEvent(T))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",d);return}console.error(d)},re={map:R,forEach:function(d,T,C){R(d,function(){T.apply(this,arguments)},C)},count:function(d){var T=0;return R(d,function(){T++}),T},toArray:function(d){return R(d,function(T){return T})||[]},only:function(d){if(!Ke(d))throw Error("React.Children.only expected to receive a single React element child.");return d}};return K.Activity=A,K.Children=re,K.Component=q,K.Fragment=L,K.Profiler=b,K.PureComponent=ve,K.StrictMode=r,K.Suspense=E,K.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=P,K.__COMPILER_RUNTIME={__proto__:null,c:function(d){return P.H.useMemoCache(d)}},K.cache=function(d){return function(){return d.apply(null,arguments)}},K.cacheSignal=function(){return null},K.cloneElement=function(d,T,C){if(d==null)throw Error("The argument must be a React element, but you passed "+d+".");var M=_e({},d.props),y=d.key;if(T!=null)for(X in T.key!==void 0&&(y=""+T.key),T)!je.call(T,X)||X==="key"||X==="__self"||X==="__source"||X==="ref"&&T.ref===void 0||(M[X]=T[X]);var X=arguments.length-2;if(X===1)M.children=C;else if(1<X){for(var J=Array(X),Ye=0;Ye<X;Ye++)J[Ye]=arguments[Ye+2];M.children=J}return $e(d.type,y,M)},K.createContext=function(d){return d={$$typeof:B,_currentValue:d,_currentValue2:d,_threadCount:0,Provider:null,Consumer:null},d.Provider=d,d.Consumer={$$typeof:H,_context:d},d},K.createElement=function(d,T,C){var M,y={},X=null;if(T!=null)for(M in T.key!==void 0&&(X=""+T.key),T)je.call(T,M)&&M!=="key"&&M!=="__self"&&M!=="__source"&&(y[M]=T[M]);var J=arguments.length-2;if(J===1)y.children=C;else if(1<J){for(var Ye=Array(J),ze=0;ze<J;ze++)Ye[ze]=arguments[ze+2];y.children=Ye}if(d&&d.defaultProps)for(M in J=d.defaultProps,J)y[M]===void 0&&(y[M]=J[M]);return $e(d,X,y)},K.createRef=function(){return{current:null}},K.forwardRef=function(d){return{$$typeof:D,render:d}},K.isValidElement=Ke,K.lazy=function(d){return{$$typeof:O,_payload:{_status:-1,_result:d},_init:k}},K.memo=function(d,T){return{$$typeof:h,type:d,compare:T===void 0?null:T}},K.startTransition=function(d){var T=P.T,C={};P.T=C;try{var M=d(),y=P.S;y!==null&&y(C,M),typeof M=="object"&&M!==null&&typeof M.then=="function"&&M.then(qe,ue)}catch(X){ue(X)}finally{T!==null&&C.types!==null&&(T.types=C.types),P.T=T}},K.unstable_useCacheRefresh=function(){return P.H.useCacheRefresh()},K.use=function(d){return P.H.use(d)},K.useActionState=function(d,T,C){return P.H.useActionState(d,T,C)},K.useCallback=function(d,T){return P.H.useCallback(d,T)},K.useContext=function(d){return P.H.useContext(d)},K.useDebugValue=function(){},K.useDeferredValue=function(d,T){return P.H.useDeferredValue(d,T)},K.useEffect=function(d,T){return P.H.useEffect(d,T)},K.useEffectEvent=function(d){return P.H.useEffectEvent(d)},K.useId=function(){return P.H.useId()},K.useImperativeHandle=function(d,T,C){return P.H.useImperativeHandle(d,T,C)},K.useInsertionEffect=function(d,T){return P.H.useInsertionEffect(d,T)},K.useLayoutEffect=function(d,T){return P.H.useLayoutEffect(d,T)},K.useMemo=function(d,T){return P.H.useMemo(d,T)},K.useOptimistic=function(d,T){return P.H.useOptimistic(d,T)},K.useReducer=function(d,T,C){return P.H.useReducer(d,T,C)},K.useRef=function(d){return P.H.useRef(d)},K.useState=function(d){return P.H.useState(d)},K.useSyncExternalStore=function(d,T,C){return P.H.useSyncExternalStore(d,T,C)},K.useTransition=function(){return P.H.useTransition()},K.version="19.2.4",K}var xd;function ms(){return xd||(xd=1,us.exports=lp()),us.exports}var G=ms(),ss={exports:{}},jn={},rs={exports:{}},fs={};var jd;function ap(){return jd||(jd=1,(function(j){function w(N,R){var k=N.length;N.push(R);e:for(;0<k;){var ue=k-1>>>1,re=N[ue];if(0<b(re,R))N[ue]=R,N[k]=re,k=ue;else break e}}function L(N){return N.length===0?null:N[0]}function r(N){if(N.length===0)return null;var R=N[0],k=N.pop();if(k!==R){N[0]=k;e:for(var ue=0,re=N.length,d=re>>>1;ue<d;){var T=2*(ue+1)-1,C=N[T],M=T+1,y=N[M];if(0>b(C,k))M<re&&0>b(y,C)?(N[ue]=y,N[M]=k,ue=M):(N[ue]=C,N[T]=k,ue=T);else if(M<re&&0>b(y,k))N[ue]=y,N[M]=k,ue=M;else break e}}return R}function b(N,R){var k=N.sortIndex-R.sortIndex;return k!==0?k:N.id-R.id}if(j.unstable_now=void 0,typeof performance=="object"&&typeof performance.now=="function"){var H=performance;j.unstable_now=function(){return H.now()}}else{var B=Date,D=B.now();j.unstable_now=function(){return B.now()-D}}var E=[],h=[],O=1,A=null,W=3,U=!1,se=!1,_e=!1,tl=!1,q=typeof setTimeout=="function"?setTimeout:null,be=typeof clearTimeout=="function"?clearTimeout:null,ve=typeof setImmediate<"u"?setImmediate:null;function ke(N){for(var R=L(h);R!==null;){if(R.callback===null)r(h);else if(R.startTime<=N)r(h),R.sortIndex=R.expirationTime,w(E,R);else break;R=L(h)}}function nl(N){if(_e=!1,ke(N),!se)if(L(E)!==null)se=!0,qe||(qe=!0,Re());else{var R=L(h);R!==null&&il(nl,R.startTime-N)}}var qe=!1,P=-1,je=5,$e=-1;function Ue(){return tl?!0:!(j.unstable_now()-$e<je)}function Ke(){if(tl=!1,qe){var N=j.unstable_now();$e=N;var R=!0;try{e:{se=!1,_e&&(_e=!1,be(P),P=-1),U=!0;var k=W;try{l:{for(ke(N),A=L(E);A!==null&&!(A.expirationTime>N&&Ue());){var ue=A.callback;if(typeof ue=="function"){A.callback=null,W=A.priorityLevel;var re=ue(A.expirationTime<=N);if(N=j.unstable_now(),typeof re=="function"){A.callback=re,ke(N),R=!0;break l}A===L(E)&&r(E),ke(N)}else r(E);A=L(E)}if(A!==null)R=!0;else{var d=L(h);d!==null&&il(nl,d.startTime-N),R=!1}}break e}finally{A=null,W=k,U=!1}R=void 0}}finally{R?Re():qe=!1}}}var Re;if(typeof ve=="function")Re=function(){ve(Ke)};else if(typeof MessageChannel<"u"){var Tl=new MessageChannel,we=Tl.port2;Tl.port1.onmessage=Ke,Re=function(){we.postMessage(null)}}else Re=function(){q(Ke,0)};function il(N,R){P=q(function(){N(j.unstable_now())},R)}j.unstable_IdlePriority=5,j.unstable_ImmediatePriority=1,j.unstable_LowPriority=4,j.unstable_NormalPriority=3,j.unstable_Profiling=null,j.unstable_UserBlockingPriority=2,j.unstable_cancelCallback=function(N){N.callback=null},j.unstable_forceFrameRate=function(N){0>N||125<N?console.error("forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"):je=0<N?Math.floor(1e3/N):5},j.unstable_getCurrentPriorityLevel=function(){return W},j.unstable_next=function(N){switch(W){case 1:case 2:case 3:var R=3;break;default:R=W}var k=W;W=R;try{return N()}finally{W=k}},j.unstable_requestPaint=function(){tl=!0},j.unstable_runWithPriority=function(N,R){switch(N){case 1:case 2:case 3:case 4:case 5:break;default:N=3}var k=W;W=N;try{return R()}finally{W=k}},j.unstable_scheduleCallback=function(N,R,k){var ue=j.unstable_now();switch(typeof k=="object"&&k!==null?(k=k.delay,k=typeof k=="number"&&0<k?ue+k:ue):k=ue,N){case 1:var re=-1;break;case 2:re=250;break;case 5:re=1073741823;break;case 4:re=1e4;break;default:re=5e3}return re=k+re,N={id:O++,callback:R,priorityLevel:N,startTime:k,expirationTime:re,sortIndex:-1},k>ue?(N.sortIndex=k,w(h,N),L(E)===null&&N===L(h)&&(_e?(be(P),P=-1):_e=!0,il(nl,k-ue))):(N.sortIndex=re,w(E,N),se||U||(se=!0,qe||(qe=!0,Re()))),N},j.unstable_shouldYield=Ue,j.unstable_wrapCallback=function(N){var R=W;return function(){var k=W;W=R;try{return N.apply(this,arguments)}finally{W=k}}}})(fs)),fs}var Sd;function tp(){return Sd||(Sd=1,rs.exports=ap()),rs.exports}var os={exports:{}},Ve={};var Nd;function np(){if(Nd)return Ve;Nd=1;var j=ms();function w(E){var h="https://react.dev/errors/"+E;if(1<arguments.length){h+="?args[]="+encodeURIComponent(arguments[1]);for(var O=2;O<arguments.length;O++)h+="&args[]="+encodeURIComponent(arguments[O])}return"Minified React error #"+E+"; visit "+h+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function L(){}var r={d:{f:L,r:function(){throw Error(w(522))},D:L,C:L,L,m:L,X:L,S:L,M:L},p:0,findDOMNode:null},b=Symbol.for("react.portal");function H(E,h,O){var A=3<arguments.length&&arguments[3]!==void 0?arguments[3]:null;return{$$typeof:b,key:A==null?null:""+A,children:E,containerInfo:h,implementation:O}}var B=j.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;function D(E,h){if(E==="font")return"";if(typeof h=="string")return h==="use-credentials"?h:""}return Ve.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE=r,Ve.createPortal=function(E,h){var O=2<arguments.length&&arguments[2]!==void 0?arguments[2]:null;if(!h||h.nodeType!==1&&h.nodeType!==9&&h.nodeType!==11)throw Error(w(299));return H(E,h,null,O)},Ve.flushSync=function(E){var h=B.T,O=r.p;try{if(B.T=null,r.p=2,E)return E()}finally{B.T=h,r.p=O,r.d.f()}},Ve.preconnect=function(E,h){typeof E=="string"&&(h?(h=h.crossOrigin,h=typeof h=="string"?h==="use-credentials"?h:"":void 0):h=null,r.d.C(E,h))},Ve.prefetchDNS=function(E){typeof E=="string"&&r.d.D(E)},Ve.preinit=function(E,h){if(typeof E=="string"&&h&&typeof h.as=="string"){var O=h.as,A=D(O,h.crossOrigin),W=typeof h.integrity=="string"?h.integrity:void 0,U=typeof h.fetchPriority=="string"?h.fetchPriority:void 0;O==="style"?r.d.S(E,typeof h.precedence=="string"?h.precedence:void 0,{crossOrigin:A,integrity:W,fetchPriority:U}):O==="script"&&r.d.X(E,{crossOrigin:A,integrity:W,fetchPriority:U,nonce:typeof h.nonce=="string"?h.nonce:void 0})}},Ve.preinitModule=function(E,h){if(typeof E=="string")if(typeof h=="object"&&h!==null){if(h.as==null||h.as==="script"){var O=D(h.as,h.crossOrigin);r.d.M(E,{crossOrigin:O,integrity:typeof h.integrity=="string"?h.integrity:void 0,nonce:typeof h.nonce=="string"?h.nonce:void 0})}}else h==null&&r.d.M(E)},Ve.preload=function(E,h){if(typeof E=="string"&&typeof h=="object"&&h!==null&&typeof h.as=="string"){var O=h.as,A=D(O,h.crossOrigin);r.d.L(E,O,{crossOrigin:A,integrity:typeof h.integrity=="string"?h.integrity:void 0,nonce:typeof h.nonce=="string"?h.nonce:void 0,type:typeof h.type=="string"?h.type:void 0,fetchPriority:typeof h.fetchPriority=="string"?h.fetchPriority:void 0,referrerPolicy:typeof h.referrerPolicy=="string"?h.referrerPolicy:void 0,imageSrcSet:typeof h.imageSrcSet=="string"?h.imageSrcSet:void 0,imageSizes:typeof h.imageSizes=="string"?h.imageSizes:void 0,media:typeof h.media=="string"?h.media:void 0})}},Ve.preloadModule=function(E,h){if(typeof E=="string")if(h){var O=D(h.as,h.crossOrigin);r.d.m(E,{as:typeof h.as=="string"&&h.as!=="script"?h.as:void 0,crossOrigin:O,integrity:typeof h.integrity=="string"?h.integrity:void 0})}else r.d.m(E)},Ve.requestFormReset=function(E){r.d.r(E)},Ve.unstable_batchedUpdates=function(E,h){return E(h)},Ve.useFormState=function(E,h,O){return B.H.useFormState(E,h,O)},Ve.useFormStatus=function(){return B.H.useHostTransitionStatus()},Ve.version="19.2.4",Ve}var _d;function ip(){if(_d)return os.exports;_d=1;function j(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(j)}catch(w){console.error(w)}}return j(),os.exports=np(),os.exports}var zd;function cp(){if(zd)return jn;zd=1;var j=tp(),w=ms(),L=ip();function r(e){var l="https://react.dev/errors/"+e;if(1<arguments.length){l+="?args[]="+encodeURIComponent(arguments[1]);for(var a=2;a<arguments.length;a++)l+="&args[]="+encodeURIComponent(arguments[a])}return"Minified React error #"+e+"; visit "+l+" for the full message or use the non-minified dev environment for full errors and additional helpful warnings."}function b(e){return!(!e||e.nodeType!==1&&e.nodeType!==9&&e.nodeType!==11)}function H(e){var l=e,a=e;if(e.alternate)for(;l.return;)l=l.return;else{e=l;do l=e,(l.flags&4098)!==0&&(a=l.return),e=l.return;while(e)}return l.tag===3?a:null}function B(e){if(e.tag===13){var l=e.memoizedState;if(l===null&&(e=e.alternate,e!==null&&(l=e.memoizedState)),l!==null)return l.dehydrated}return null}function D(e){if(e.tag===31){var l=e.memoizedState;if(l===null&&(e=e.alternate,e!==null&&(l=e.memoizedState)),l!==null)return l.dehydrated}return null}function E(e){if(H(e)!==e)throw Error(r(188))}function h(e){var l=e.alternate;if(!l){if(l=H(e),l===null)throw Error(r(188));return l!==e?null:e}for(var a=e,t=l;;){var n=a.return;if(n===null)break;var i=n.alternate;if(i===null){if(t=n.return,t!==null){a=t;continue}break}if(n.child===i.child){for(i=n.child;i;){if(i===a)return E(n),e;if(i===t)return E(n),l;i=i.sibling}throw Error(r(188))}if(a.return!==t.return)a=n,t=i;else{for(var u=!1,s=n.child;s;){if(s===a){u=!0,a=n,t=i;break}if(s===t){u=!0,t=n,a=i;break}s=s.sibling}if(!u){for(s=i.child;s;){if(s===a){u=!0,a=i,t=n;break}if(s===t){u=!0,t=i,a=n;break}s=s.sibling}if(!u)throw Error(r(189))}}if(a.alternate!==t)throw Error(r(190))}if(a.tag!==3)throw Error(r(188));return a.stateNode.current===a?e:l}function O(e){var l=e.tag;if(l===5||l===26||l===27||l===6)return e;for(e=e.child;e!==null;){if(l=O(e),l!==null)return l;e=e.sibling}return null}var A=Object.assign,W=Symbol.for("react.element"),U=Symbol.for("react.transitional.element"),se=Symbol.for("react.portal"),_e=Symbol.for("react.fragment"),tl=Symbol.for("react.strict_mode"),q=Symbol.for("react.profiler"),be=Symbol.for("react.consumer"),ve=Symbol.for("react.context"),ke=Symbol.for("react.forward_ref"),nl=Symbol.for("react.suspense"),qe=Symbol.for("react.suspense_list"),P=Symbol.for("react.memo"),je=Symbol.for("react.lazy"),$e=Symbol.for("react.activity"),Ue=Symbol.for("react.memo_cache_sentinel"),Ke=Symbol.iterator;function Re(e){return e===null||typeof e!="object"?null:(e=Ke&&e[Ke]||e["@@iterator"],typeof e=="function"?e:null)}var Tl=Symbol.for("react.client.reference");function we(e){if(e==null)return null;if(typeof e=="function")return e.$$typeof===Tl?null:e.displayName||e.name||null;if(typeof e=="string")return e;switch(e){case _e:return"Fragment";case q:return"Profiler";case tl:return"StrictMode";case nl:return"Suspense";case qe:return"SuspenseList";case $e:return"Activity"}if(typeof e=="object")switch(e.$$typeof){case se:return"Portal";case ve:return e.displayName||"Context";case be:return(e._context.displayName||"Context")+".Consumer";case ke:var l=e.render;return e=e.displayName,e||(e=l.displayName||l.name||"",e=e!==""?"ForwardRef("+e+")":"ForwardRef"),e;case P:return l=e.displayName||null,l!==null?l:we(e.type)||"Memo";case je:l=e._payload,e=e._init;try{return we(e(l))}catch{}}return null}var il=Array.isArray,N=w.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,R=L.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE,k={pending:!1,data:null,method:null,action:null},ue=[],re=-1;function d(e){return{current:e}}function T(e){0>re||(e.current=ue[re],ue[re]=null,re--)}function C(e,l){re++,ue[re]=e.current,e.current=l}var M=d(null),y=d(null),X=d(null),J=d(null);function Ye(e,l){switch(C(X,l),C(y,e),C(M,null),l.nodeType){case 9:case 11:e=(e=l.documentElement)&&(e=e.namespaceURI)?Xo(e):0;break;default:if(e=l.tagName,l=l.namespaceURI)l=Xo(l),e=Qo(l,e);else switch(e){case"svg":e=1;break;case"math":e=2;break;default:e=0}}T(M),C(M,e)}function ze(){T(M),T(y),T(X)}function Tt(e){e.memoizedState!==null&&C(J,e);var l=M.current,a=Qo(l,e.type);l!==a&&(C(y,e),C(M,a))}function Sn(e){y.current===e&&(T(M),T(y)),J.current===e&&(T(J),vn._currentValue=k)}var Li,hs;function Na(e){if(Li===void 0)try{throw Error()}catch(a){var l=a.stack.trim().match(/\n( *(at )?)/);Li=l&&l[1]||"",hs=-1<a.stack.indexOf(`
    at`)?" (<anonymous>)":-1<a.stack.indexOf("@")?"@unknown:0:0":""}return`
`+Li+e+hs}var Zi=!1;function wi(e,l){if(!e||Zi)return"";Zi=!0;var a=Error.prepareStackTrace;Error.prepareStackTrace=void 0;try{var t={DetermineComponentFrameRoot:function(){try{if(l){var z=function(){throw Error()};if(Object.defineProperty(z.prototype,"props",{set:function(){throw Error()}}),typeof Reflect=="object"&&Reflect.construct){try{Reflect.construct(z,[])}catch(x){var g=x}Reflect.construct(e,[],z)}else{try{z.call()}catch(x){g=x}e.call(z.prototype)}}else{try{throw Error()}catch(x){g=x}(z=e())&&typeof z.catch=="function"&&z.catch(function(){})}}catch(x){if(x&&g&&typeof x.stack=="string")return[x.stack,g.stack]}return[null,null]}};t.DetermineComponentFrameRoot.displayName="DetermineComponentFrameRoot";var n=Object.getOwnPropertyDescriptor(t.DetermineComponentFrameRoot,"name");n&&n.configurable&&Object.defineProperty(t.DetermineComponentFrameRoot,"name",{value:"DetermineComponentFrameRoot"});var i=t.DetermineComponentFrameRoot(),u=i[0],s=i[1];if(u&&s){var f=u.split(`
`),v=s.split(`
`);for(n=t=0;t<f.length&&!f[t].includes("DetermineComponentFrameRoot");)t++;for(;n<v.length&&!v[n].includes("DetermineComponentFrameRoot");)n++;if(t===f.length||n===v.length)for(t=f.length-1,n=v.length-1;1<=t&&0<=n&&f[t]!==v[n];)n--;for(;1<=t&&0<=n;t--,n--)if(f[t]!==v[n]){if(t!==1||n!==1)do if(t--,n--,0>n||f[t]!==v[n]){var S=`
`+f[t].replace(" at new "," at ");return e.displayName&&S.includes("<anonymous>")&&(S=S.replace("<anonymous>",e.displayName)),S}while(1<=t&&0<=n);break}}}finally{Zi=!1,Error.prepareStackTrace=a}return(a=e?e.displayName||e.name:"")?Na(a):""}function Dd(e,l){switch(e.tag){case 26:case 27:case 5:return Na(e.type);case 16:return Na("Lazy");case 13:return e.child!==l&&l!==null?Na("Suspense Fallback"):Na("Suspense");case 19:return Na("SuspenseList");case 0:case 15:return wi(e.type,!1);case 11:return wi(e.type.render,!1);case 1:return wi(e.type,!0);case 31:return Na("Activity");default:return""}}function ps(e){try{var l="",a=null;do l+=Dd(e,a),a=e,e=e.return;while(e);return l}catch(t){return`
Error generating stack: `+t.message+`
`+t.stack}}var Vi=Object.prototype.hasOwnProperty,ki=j.unstable_scheduleCallback,Ki=j.unstable_cancelCallback,Md=j.unstable_shouldYield,Ud=j.unstable_requestPaint,cl=j.unstable_now,Cd=j.unstable_getCurrentPriorityLevel,vs=j.unstable_ImmediatePriority,gs=j.unstable_UserBlockingPriority,Nn=j.unstable_NormalPriority,Rd=j.unstable_LowPriority,ys=j.unstable_IdlePriority,Hd=j.log,Bd=j.unstable_setDisableYieldValue,Et=null,ul=null;function Pl(e){if(typeof Hd=="function"&&Bd(e),ul&&typeof ul.setStrictMode=="function")try{ul.setStrictMode(Et,e)}catch{}}var sl=Math.clz32?Math.clz32:Gd,qd=Math.log,Yd=Math.LN2;function Gd(e){return e>>>=0,e===0?32:31-(qd(e)/Yd|0)|0}var _n=256,zn=262144,Tn=4194304;function _a(e){var l=e&42;if(l!==0)return l;switch(e&-e){case 1:return 1;case 2:return 2;case 4:return 4;case 8:return 8;case 16:return 16;case 32:return 32;case 64:return 64;case 128:return 128;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:return e&261888;case 262144:case 524288:case 1048576:case 2097152:return e&3932160;case 4194304:case 8388608:case 16777216:case 33554432:return e&62914560;case 67108864:return 67108864;case 134217728:return 134217728;case 268435456:return 268435456;case 536870912:return 536870912;case 1073741824:return 0;default:return e}}function En(e,l,a){var t=e.pendingLanes;if(t===0)return 0;var n=0,i=e.suspendedLanes,u=e.pingedLanes;e=e.warmLanes;var s=t&134217727;return s!==0?(t=s&~i,t!==0?n=_a(t):(u&=s,u!==0?n=_a(u):a||(a=s&~e,a!==0&&(n=_a(a))))):(s=t&~i,s!==0?n=_a(s):u!==0?n=_a(u):a||(a=t&~e,a!==0&&(n=_a(a)))),n===0?0:l!==0&&l!==n&&(l&i)===0&&(i=n&-n,a=l&-l,i>=a||i===32&&(a&4194048)!==0)?l:n}function At(e,l){return(e.pendingLanes&~(e.suspendedLanes&~e.pingedLanes)&l)===0}function Xd(e,l){switch(e){case 1:case 2:case 4:case 8:case 64:return l+250;case 16:case 32:case 128:case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:return l+5e3;case 4194304:case 8388608:case 16777216:case 33554432:return-1;case 67108864:case 134217728:case 268435456:case 536870912:case 1073741824:return-1;default:return-1}}function bs(){var e=Tn;return Tn<<=1,(Tn&62914560)===0&&(Tn=4194304),e}function Ji(e){for(var l=[],a=0;31>a;a++)l.push(e);return l}function Ot(e,l){e.pendingLanes|=l,l!==268435456&&(e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0)}function Qd(e,l,a,t,n,i){var u=e.pendingLanes;e.pendingLanes=a,e.suspendedLanes=0,e.pingedLanes=0,e.warmLanes=0,e.expiredLanes&=a,e.entangledLanes&=a,e.errorRecoveryDisabledLanes&=a,e.shellSuspendCounter=0;var s=e.entanglements,f=e.expirationTimes,v=e.hiddenUpdates;for(a=u&~a;0<a;){var S=31-sl(a),z=1<<S;s[S]=0,f[S]=-1;var g=v[S];if(g!==null)for(v[S]=null,S=0;S<g.length;S++){var x=g[S];x!==null&&(x.lane&=-536870913)}a&=~z}t!==0&&xs(e,t,0),i!==0&&n===0&&e.tag!==0&&(e.suspendedLanes|=i&~(u&~l))}function xs(e,l,a){e.pendingLanes|=l,e.suspendedLanes&=~l;var t=31-sl(l);e.entangledLanes|=l,e.entanglements[t]=e.entanglements[t]|1073741824|a&261930}function js(e,l){var a=e.entangledLanes|=l;for(e=e.entanglements;a;){var t=31-sl(a),n=1<<t;n&l|e[t]&l&&(e[t]|=l),a&=~n}}function Ss(e,l){var a=l&-l;return a=(a&42)!==0?1:$i(a),(a&(e.suspendedLanes|l))!==0?0:a}function $i(e){switch(e){case 2:e=1;break;case 8:e=4;break;case 32:e=16;break;case 256:case 512:case 1024:case 2048:case 4096:case 8192:case 16384:case 32768:case 65536:case 131072:case 262144:case 524288:case 1048576:case 2097152:case 4194304:case 8388608:case 16777216:case 33554432:e=128;break;case 268435456:e=134217728;break;default:e=0}return e}function Wi(e){return e&=-e,2<e?8<e?(e&134217727)!==0?32:268435456:8:2}function Ns(){var e=R.p;return e!==0?e:(e=window.event,e===void 0?32:fd(e.type))}function _s(e,l){var a=R.p;try{return R.p=e,l()}finally{R.p=a}}var Il=Math.random().toString(36).slice(2),Ge="__reactFiber$"+Il,We="__reactProps$"+Il,La="__reactContainer$"+Il,Fi="__reactEvents$"+Il,Ld="__reactListeners$"+Il,Zd="__reactHandles$"+Il,zs="__reactResources$"+Il,Dt="__reactMarker$"+Il;function Pi(e){delete e[Ge],delete e[We],delete e[Fi],delete e[Ld],delete e[Zd]}function Za(e){var l=e[Ge];if(l)return l;for(var a=e.parentNode;a;){if(l=a[La]||a[Ge]){if(a=l.alternate,l.child!==null||a!==null&&a.child!==null)for(e=Jo(e);e!==null;){if(a=e[Ge])return a;e=Jo(e)}return l}e=a,a=e.parentNode}return null}function wa(e){if(e=e[Ge]||e[La]){var l=e.tag;if(l===5||l===6||l===13||l===31||l===26||l===27||l===3)return e}return null}function Mt(e){var l=e.tag;if(l===5||l===26||l===27||l===6)return e.stateNode;throw Error(r(33))}function Va(e){var l=e[zs];return l||(l=e[zs]={hoistableStyles:new Map,hoistableScripts:new Map}),l}function He(e){e[Dt]=!0}var Ts=new Set,Es={};function za(e,l){ka(e,l),ka(e+"Capture",l)}function ka(e,l){for(Es[e]=l,e=0;e<l.length;e++)Ts.add(l[e])}var wd=RegExp("^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"),As={},Os={};function Vd(e){return Vi.call(Os,e)?!0:Vi.call(As,e)?!1:wd.test(e)?Os[e]=!0:(As[e]=!0,!1)}function An(e,l,a){if(Vd(l))if(a===null)e.removeAttribute(l);else{switch(typeof a){case"undefined":case"function":case"symbol":e.removeAttribute(l);return;case"boolean":var t=l.toLowerCase().slice(0,5);if(t!=="data-"&&t!=="aria-"){e.removeAttribute(l);return}}e.setAttribute(l,""+a)}}function On(e,l,a){if(a===null)e.removeAttribute(l);else{switch(typeof a){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(l);return}e.setAttribute(l,""+a)}}function Rl(e,l,a,t){if(t===null)e.removeAttribute(a);else{switch(typeof t){case"undefined":case"function":case"symbol":case"boolean":e.removeAttribute(a);return}e.setAttributeNS(l,a,""+t)}}function vl(e){switch(typeof e){case"bigint":case"boolean":case"number":case"string":case"undefined":return e;case"object":return e;default:return""}}function Ds(e){var l=e.type;return(e=e.nodeName)&&e.toLowerCase()==="input"&&(l==="checkbox"||l==="radio")}function kd(e,l,a){var t=Object.getOwnPropertyDescriptor(e.constructor.prototype,l);if(!e.hasOwnProperty(l)&&typeof t<"u"&&typeof t.get=="function"&&typeof t.set=="function"){var n=t.get,i=t.set;return Object.defineProperty(e,l,{configurable:!0,get:function(){return n.call(this)},set:function(u){a=""+u,i.call(this,u)}}),Object.defineProperty(e,l,{enumerable:t.enumerable}),{getValue:function(){return a},setValue:function(u){a=""+u},stopTracking:function(){e._valueTracker=null,delete e[l]}}}}function Ii(e){if(!e._valueTracker){var l=Ds(e)?"checked":"value";e._valueTracker=kd(e,l,""+e[l])}}function Ms(e){if(!e)return!1;var l=e._valueTracker;if(!l)return!0;var a=l.getValue(),t="";return e&&(t=Ds(e)?e.checked?"true":"false":e.value),e=t,e!==a?(l.setValue(e),!0):!1}function Dn(e){if(e=e||(typeof document<"u"?document:void 0),typeof e>"u")return null;try{return e.activeElement||e.body}catch{return e.body}}var Kd=/[\n"\\]/g;function gl(e){return e.replace(Kd,function(l){return"\\"+l.charCodeAt(0).toString(16)+" "})}function ec(e,l,a,t,n,i,u,s){e.name="",u!=null&&typeof u!="function"&&typeof u!="symbol"&&typeof u!="boolean"?e.type=u:e.removeAttribute("type"),l!=null?u==="number"?(l===0&&e.value===""||e.value!=l)&&(e.value=""+vl(l)):e.value!==""+vl(l)&&(e.value=""+vl(l)):u!=="submit"&&u!=="reset"||e.removeAttribute("value"),l!=null?lc(e,u,vl(l)):a!=null?lc(e,u,vl(a)):t!=null&&e.removeAttribute("value"),n==null&&i!=null&&(e.defaultChecked=!!i),n!=null&&(e.checked=n&&typeof n!="function"&&typeof n!="symbol"),s!=null&&typeof s!="function"&&typeof s!="symbol"&&typeof s!="boolean"?e.name=""+vl(s):e.removeAttribute("name")}function Us(e,l,a,t,n,i,u,s){if(i!=null&&typeof i!="function"&&typeof i!="symbol"&&typeof i!="boolean"&&(e.type=i),l!=null||a!=null){if(!(i!=="submit"&&i!=="reset"||l!=null)){Ii(e);return}a=a!=null?""+vl(a):"",l=l!=null?""+vl(l):a,s||l===e.value||(e.value=l),e.defaultValue=l}t=t??n,t=typeof t!="function"&&typeof t!="symbol"&&!!t,e.checked=s?e.checked:!!t,e.defaultChecked=!!t,u!=null&&typeof u!="function"&&typeof u!="symbol"&&typeof u!="boolean"&&(e.name=u),Ii(e)}function lc(e,l,a){l==="number"&&Dn(e.ownerDocument)===e||e.defaultValue===""+a||(e.defaultValue=""+a)}function Ka(e,l,a,t){if(e=e.options,l){l={};for(var n=0;n<a.length;n++)l["$"+a[n]]=!0;for(a=0;a<e.length;a++)n=l.hasOwnProperty("$"+e[a].value),e[a].selected!==n&&(e[a].selected=n),n&&t&&(e[a].defaultSelected=!0)}else{for(a=""+vl(a),l=null,n=0;n<e.length;n++){if(e[n].value===a){e[n].selected=!0,t&&(e[n].defaultSelected=!0);return}l!==null||e[n].disabled||(l=e[n])}l!==null&&(l.selected=!0)}}function Cs(e,l,a){if(l!=null&&(l=""+vl(l),l!==e.value&&(e.value=l),a==null)){e.defaultValue!==l&&(e.defaultValue=l);return}e.defaultValue=a!=null?""+vl(a):""}function Rs(e,l,a,t){if(l==null){if(t!=null){if(a!=null)throw Error(r(92));if(il(t)){if(1<t.length)throw Error(r(93));t=t[0]}a=t}a==null&&(a=""),l=a}a=vl(l),e.defaultValue=a,t=e.textContent,t===a&&t!==""&&t!==null&&(e.value=t),Ii(e)}function Ja(e,l){if(l){var a=e.firstChild;if(a&&a===e.lastChild&&a.nodeType===3){a.nodeValue=l;return}}e.textContent=l}var Jd=new Set("animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(" "));function Hs(e,l,a){var t=l.indexOf("--")===0;a==null||typeof a=="boolean"||a===""?t?e.setProperty(l,""):l==="float"?e.cssFloat="":e[l]="":t?e.setProperty(l,a):typeof a!="number"||a===0||Jd.has(l)?l==="float"?e.cssFloat=a:e[l]=(""+a).trim():e[l]=a+"px"}function Bs(e,l,a){if(l!=null&&typeof l!="object")throw Error(r(62));if(e=e.style,a!=null){for(var t in a)!a.hasOwnProperty(t)||l!=null&&l.hasOwnProperty(t)||(t.indexOf("--")===0?e.setProperty(t,""):t==="float"?e.cssFloat="":e[t]="");for(var n in l)t=l[n],l.hasOwnProperty(n)&&a[n]!==t&&Hs(e,n,t)}else for(var i in l)l.hasOwnProperty(i)&&Hs(e,i,l[i])}function ac(e){if(e.indexOf("-")===-1)return!1;switch(e){case"annotation-xml":case"color-profile":case"font-face":case"font-face-src":case"font-face-uri":case"font-face-format":case"font-face-name":case"missing-glyph":return!1;default:return!0}}var $d=new Map([["acceptCharset","accept-charset"],["htmlFor","for"],["httpEquiv","http-equiv"],["crossOrigin","crossorigin"],["accentHeight","accent-height"],["alignmentBaseline","alignment-baseline"],["arabicForm","arabic-form"],["baselineShift","baseline-shift"],["capHeight","cap-height"],["clipPath","clip-path"],["clipRule","clip-rule"],["colorInterpolation","color-interpolation"],["colorInterpolationFilters","color-interpolation-filters"],["colorProfile","color-profile"],["colorRendering","color-rendering"],["dominantBaseline","dominant-baseline"],["enableBackground","enable-background"],["fillOpacity","fill-opacity"],["fillRule","fill-rule"],["floodColor","flood-color"],["floodOpacity","flood-opacity"],["fontFamily","font-family"],["fontSize","font-size"],["fontSizeAdjust","font-size-adjust"],["fontStretch","font-stretch"],["fontStyle","font-style"],["fontVariant","font-variant"],["fontWeight","font-weight"],["glyphName","glyph-name"],["glyphOrientationHorizontal","glyph-orientation-horizontal"],["glyphOrientationVertical","glyph-orientation-vertical"],["horizAdvX","horiz-adv-x"],["horizOriginX","horiz-origin-x"],["imageRendering","image-rendering"],["letterSpacing","letter-spacing"],["lightingColor","lighting-color"],["markerEnd","marker-end"],["markerMid","marker-mid"],["markerStart","marker-start"],["overlinePosition","overline-position"],["overlineThickness","overline-thickness"],["paintOrder","paint-order"],["panose-1","panose-1"],["pointerEvents","pointer-events"],["renderingIntent","rendering-intent"],["shapeRendering","shape-rendering"],["stopColor","stop-color"],["stopOpacity","stop-opacity"],["strikethroughPosition","strikethrough-position"],["strikethroughThickness","strikethrough-thickness"],["strokeDasharray","stroke-dasharray"],["strokeDashoffset","stroke-dashoffset"],["strokeLinecap","stroke-linecap"],["strokeLinejoin","stroke-linejoin"],["strokeMiterlimit","stroke-miterlimit"],["strokeOpacity","stroke-opacity"],["strokeWidth","stroke-width"],["textAnchor","text-anchor"],["textDecoration","text-decoration"],["textRendering","text-rendering"],["transformOrigin","transform-origin"],["underlinePosition","underline-position"],["underlineThickness","underline-thickness"],["unicodeBidi","unicode-bidi"],["unicodeRange","unicode-range"],["unitsPerEm","units-per-em"],["vAlphabetic","v-alphabetic"],["vHanging","v-hanging"],["vIdeographic","v-ideographic"],["vMathematical","v-mathematical"],["vectorEffect","vector-effect"],["vertAdvY","vert-adv-y"],["vertOriginX","vert-origin-x"],["vertOriginY","vert-origin-y"],["wordSpacing","word-spacing"],["writingMode","writing-mode"],["xmlnsXlink","xmlns:xlink"],["xHeight","x-height"]]),Wd=/^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;function Mn(e){return Wd.test(""+e)?"javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')":e}function Hl(){}var tc=null;function nc(e){return e=e.target||e.srcElement||window,e.correspondingUseElement&&(e=e.correspondingUseElement),e.nodeType===3?e.parentNode:e}var $a=null,Wa=null;function qs(e){var l=wa(e);if(l&&(e=l.stateNode)){var a=e[We]||null;e:switch(e=l.stateNode,l.type){case"input":if(ec(e,a.value,a.defaultValue,a.defaultValue,a.checked,a.defaultChecked,a.type,a.name),l=a.name,a.type==="radio"&&l!=null){for(a=e;a.parentNode;)a=a.parentNode;for(a=a.querySelectorAll('input[name="'+gl(""+l)+'"][type="radio"]'),l=0;l<a.length;l++){var t=a[l];if(t!==e&&t.form===e.form){var n=t[We]||null;if(!n)throw Error(r(90));ec(t,n.value,n.defaultValue,n.defaultValue,n.checked,n.defaultChecked,n.type,n.name)}}for(l=0;l<a.length;l++)t=a[l],t.form===e.form&&Ms(t)}break e;case"textarea":Cs(e,a.value,a.defaultValue);break e;case"select":l=a.value,l!=null&&Ka(e,!!a.multiple,l,!1)}}}var ic=!1;function Ys(e,l,a){if(ic)return e(l,a);ic=!0;try{var t=e(l);return t}finally{if(ic=!1,($a!==null||Wa!==null)&&(yi(),$a&&(l=$a,e=Wa,Wa=$a=null,qs(l),e)))for(l=0;l<e.length;l++)qs(e[l])}}function Ut(e,l){var a=e.stateNode;if(a===null)return null;var t=a[We]||null;if(t===null)return null;a=t[l];e:switch(l){case"onClick":case"onClickCapture":case"onDoubleClick":case"onDoubleClickCapture":case"onMouseDown":case"onMouseDownCapture":case"onMouseMove":case"onMouseMoveCapture":case"onMouseUp":case"onMouseUpCapture":case"onMouseEnter":(t=!t.disabled)||(e=e.type,t=!(e==="button"||e==="input"||e==="select"||e==="textarea")),e=!t;break e;default:e=!1}if(e)return null;if(a&&typeof a!="function")throw Error(r(231,l,typeof a));return a}var Bl=!(typeof window>"u"||typeof window.document>"u"||typeof window.document.createElement>"u"),cc=!1;if(Bl)try{var Ct={};Object.defineProperty(Ct,"passive",{get:function(){cc=!0}}),window.addEventListener("test",Ct,Ct),window.removeEventListener("test",Ct,Ct)}catch{cc=!1}var ea=null,uc=null,Un=null;function Gs(){if(Un)return Un;var e,l=uc,a=l.length,t,n="value"in ea?ea.value:ea.textContent,i=n.length;for(e=0;e<a&&l[e]===n[e];e++);var u=a-e;for(t=1;t<=u&&l[a-t]===n[i-t];t++);return Un=n.slice(e,1<t?1-t:void 0)}function Cn(e){var l=e.keyCode;return"charCode"in e?(e=e.charCode,e===0&&l===13&&(e=13)):e=l,e===10&&(e=13),32<=e||e===13?e:0}function Rn(){return!0}function Xs(){return!1}function Fe(e){function l(a,t,n,i,u){this._reactName=a,this._targetInst=n,this.type=t,this.nativeEvent=i,this.target=u,this.currentTarget=null;for(var s in e)e.hasOwnProperty(s)&&(a=e[s],this[s]=a?a(i):i[s]);return this.isDefaultPrevented=(i.defaultPrevented!=null?i.defaultPrevented:i.returnValue===!1)?Rn:Xs,this.isPropagationStopped=Xs,this}return A(l.prototype,{preventDefault:function(){this.defaultPrevented=!0;var a=this.nativeEvent;a&&(a.preventDefault?a.preventDefault():typeof a.returnValue!="unknown"&&(a.returnValue=!1),this.isDefaultPrevented=Rn)},stopPropagation:function(){var a=this.nativeEvent;a&&(a.stopPropagation?a.stopPropagation():typeof a.cancelBubble!="unknown"&&(a.cancelBubble=!0),this.isPropagationStopped=Rn)},persist:function(){},isPersistent:Rn}),l}var Ta={eventPhase:0,bubbles:0,cancelable:0,timeStamp:function(e){return e.timeStamp||Date.now()},defaultPrevented:0,isTrusted:0},Hn=Fe(Ta),Rt=A({},Ta,{view:0,detail:0}),Fd=Fe(Rt),sc,rc,Ht,Bn=A({},Rt,{screenX:0,screenY:0,clientX:0,clientY:0,pageX:0,pageY:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,getModifierState:oc,button:0,buttons:0,relatedTarget:function(e){return e.relatedTarget===void 0?e.fromElement===e.srcElement?e.toElement:e.fromElement:e.relatedTarget},movementX:function(e){return"movementX"in e?e.movementX:(e!==Ht&&(Ht&&e.type==="mousemove"?(sc=e.screenX-Ht.screenX,rc=e.screenY-Ht.screenY):rc=sc=0,Ht=e),sc)},movementY:function(e){return"movementY"in e?e.movementY:rc}}),Qs=Fe(Bn),Pd=A({},Bn,{dataTransfer:0}),Id=Fe(Pd),em=A({},Rt,{relatedTarget:0}),fc=Fe(em),lm=A({},Ta,{animationName:0,elapsedTime:0,pseudoElement:0}),am=Fe(lm),tm=A({},Ta,{clipboardData:function(e){return"clipboardData"in e?e.clipboardData:window.clipboardData}}),nm=Fe(tm),im=A({},Ta,{data:0}),Ls=Fe(im),cm={Esc:"Escape",Spacebar:" ",Left:"ArrowLeft",Up:"ArrowUp",Right:"ArrowRight",Down:"ArrowDown",Del:"Delete",Win:"OS",Menu:"ContextMenu",Apps:"ContextMenu",Scroll:"ScrollLock",MozPrintableKey:"Unidentified"},um={8:"Backspace",9:"Tab",12:"Clear",13:"Enter",16:"Shift",17:"Control",18:"Alt",19:"Pause",20:"CapsLock",27:"Escape",32:" ",33:"PageUp",34:"PageDown",35:"End",36:"Home",37:"ArrowLeft",38:"ArrowUp",39:"ArrowRight",40:"ArrowDown",45:"Insert",46:"Delete",112:"F1",113:"F2",114:"F3",115:"F4",116:"F5",117:"F6",118:"F7",119:"F8",120:"F9",121:"F10",122:"F11",123:"F12",144:"NumLock",145:"ScrollLock",224:"Meta"},sm={Alt:"altKey",Control:"ctrlKey",Meta:"metaKey",Shift:"shiftKey"};function rm(e){var l=this.nativeEvent;return l.getModifierState?l.getModifierState(e):(e=sm[e])?!!l[e]:!1}function oc(){return rm}var fm=A({},Rt,{key:function(e){if(e.key){var l=cm[e.key]||e.key;if(l!=="Unidentified")return l}return e.type==="keypress"?(e=Cn(e),e===13?"Enter":String.fromCharCode(e)):e.type==="keydown"||e.type==="keyup"?um[e.keyCode]||"Unidentified":""},code:0,location:0,ctrlKey:0,shiftKey:0,altKey:0,metaKey:0,repeat:0,locale:0,getModifierState:oc,charCode:function(e){return e.type==="keypress"?Cn(e):0},keyCode:function(e){return e.type==="keydown"||e.type==="keyup"?e.keyCode:0},which:function(e){return e.type==="keypress"?Cn(e):e.type==="keydown"||e.type==="keyup"?e.keyCode:0}}),om=Fe(fm),dm=A({},Bn,{pointerId:0,width:0,height:0,pressure:0,tangentialPressure:0,tiltX:0,tiltY:0,twist:0,pointerType:0,isPrimary:0}),Zs=Fe(dm),mm=A({},Rt,{touches:0,targetTouches:0,changedTouches:0,altKey:0,metaKey:0,ctrlKey:0,shiftKey:0,getModifierState:oc}),hm=Fe(mm),pm=A({},Ta,{propertyName:0,elapsedTime:0,pseudoElement:0}),vm=Fe(pm),gm=A({},Bn,{deltaX:function(e){return"deltaX"in e?e.deltaX:"wheelDeltaX"in e?-e.wheelDeltaX:0},deltaY:function(e){return"deltaY"in e?e.deltaY:"wheelDeltaY"in e?-e.wheelDeltaY:"wheelDelta"in e?-e.wheelDelta:0},deltaZ:0,deltaMode:0}),ym=Fe(gm),bm=A({},Ta,{newState:0,oldState:0}),xm=Fe(bm),jm=[9,13,27,32],dc=Bl&&"CompositionEvent"in window,Bt=null;Bl&&"documentMode"in document&&(Bt=document.documentMode);var Sm=Bl&&"TextEvent"in window&&!Bt,ws=Bl&&(!dc||Bt&&8<Bt&&11>=Bt),Vs=" ",ks=!1;function Ks(e,l){switch(e){case"keyup":return jm.indexOf(l.keyCode)!==-1;case"keydown":return l.keyCode!==229;case"keypress":case"mousedown":case"focusout":return!0;default:return!1}}function Js(e){return e=e.detail,typeof e=="object"&&"data"in e?e.data:null}var Fa=!1;function Nm(e,l){switch(e){case"compositionend":return Js(l);case"keypress":return l.which!==32?null:(ks=!0,Vs);case"textInput":return e=l.data,e===Vs&&ks?null:e;default:return null}}function _m(e,l){if(Fa)return e==="compositionend"||!dc&&Ks(e,l)?(e=Gs(),Un=uc=ea=null,Fa=!1,e):null;switch(e){case"paste":return null;case"keypress":if(!(l.ctrlKey||l.altKey||l.metaKey)||l.ctrlKey&&l.altKey){if(l.char&&1<l.char.length)return l.char;if(l.which)return String.fromCharCode(l.which)}return null;case"compositionend":return ws&&l.locale!=="ko"?null:l.data;default:return null}}var zm={color:!0,date:!0,datetime:!0,"datetime-local":!0,email:!0,month:!0,number:!0,password:!0,range:!0,search:!0,tel:!0,text:!0,time:!0,url:!0,week:!0};function $s(e){var l=e&&e.nodeName&&e.nodeName.toLowerCase();return l==="input"?!!zm[e.type]:l==="textarea"}function Ws(e,l,a,t){$a?Wa?Wa.push(t):Wa=[t]:$a=t,l=zi(l,"onChange"),0<l.length&&(a=new Hn("onChange","change",null,a,t),e.push({event:a,listeners:l}))}var qt=null,Yt=null;function Tm(e){Ro(e,0)}function qn(e){var l=Mt(e);if(Ms(l))return e}function Fs(e,l){if(e==="change")return l}var Ps=!1;if(Bl){var mc;if(Bl){var hc="oninput"in document;if(!hc){var Is=document.createElement("div");Is.setAttribute("oninput","return;"),hc=typeof Is.oninput=="function"}mc=hc}else mc=!1;Ps=mc&&(!document.documentMode||9<document.documentMode)}function er(){qt&&(qt.detachEvent("onpropertychange",lr),Yt=qt=null)}function lr(e){if(e.propertyName==="value"&&qn(Yt)){var l=[];Ws(l,Yt,e,nc(e)),Ys(Tm,l)}}function Em(e,l,a){e==="focusin"?(er(),qt=l,Yt=a,qt.attachEvent("onpropertychange",lr)):e==="focusout"&&er()}function Am(e){if(e==="selectionchange"||e==="keyup"||e==="keydown")return qn(Yt)}function Om(e,l){if(e==="click")return qn(l)}function Dm(e,l){if(e==="input"||e==="change")return qn(l)}function Mm(e,l){return e===l&&(e!==0||1/e===1/l)||e!==e&&l!==l}var rl=typeof Object.is=="function"?Object.is:Mm;function Gt(e,l){if(rl(e,l))return!0;if(typeof e!="object"||e===null||typeof l!="object"||l===null)return!1;var a=Object.keys(e),t=Object.keys(l);if(a.length!==t.length)return!1;for(t=0;t<a.length;t++){var n=a[t];if(!Vi.call(l,n)||!rl(e[n],l[n]))return!1}return!0}function ar(e){for(;e&&e.firstChild;)e=e.firstChild;return e}function tr(e,l){var a=ar(e);e=0;for(var t;a;){if(a.nodeType===3){if(t=e+a.textContent.length,e<=l&&t>=l)return{node:a,offset:l-e};e=t}e:{for(;a;){if(a.nextSibling){a=a.nextSibling;break e}a=a.parentNode}a=void 0}a=ar(a)}}function nr(e,l){return e&&l?e===l?!0:e&&e.nodeType===3?!1:l&&l.nodeType===3?nr(e,l.parentNode):"contains"in e?e.contains(l):e.compareDocumentPosition?!!(e.compareDocumentPosition(l)&16):!1:!1}function ir(e){e=e!=null&&e.ownerDocument!=null&&e.ownerDocument.defaultView!=null?e.ownerDocument.defaultView:window;for(var l=Dn(e.document);l instanceof e.HTMLIFrameElement;){try{var a=typeof l.contentWindow.location.href=="string"}catch{a=!1}if(a)e=l.contentWindow;else break;l=Dn(e.document)}return l}function pc(e){var l=e&&e.nodeName&&e.nodeName.toLowerCase();return l&&(l==="input"&&(e.type==="text"||e.type==="search"||e.type==="tel"||e.type==="url"||e.type==="password")||l==="textarea"||e.contentEditable==="true")}var Um=Bl&&"documentMode"in document&&11>=document.documentMode,Pa=null,vc=null,Xt=null,gc=!1;function cr(e,l,a){var t=a.window===a?a.document:a.nodeType===9?a:a.ownerDocument;gc||Pa==null||Pa!==Dn(t)||(t=Pa,"selectionStart"in t&&pc(t)?t={start:t.selectionStart,end:t.selectionEnd}:(t=(t.ownerDocument&&t.ownerDocument.defaultView||window).getSelection(),t={anchorNode:t.anchorNode,anchorOffset:t.anchorOffset,focusNode:t.focusNode,focusOffset:t.focusOffset}),Xt&&Gt(Xt,t)||(Xt=t,t=zi(vc,"onSelect"),0<t.length&&(l=new Hn("onSelect","select",null,l,a),e.push({event:l,listeners:t}),l.target=Pa)))}function Ea(e,l){var a={};return a[e.toLowerCase()]=l.toLowerCase(),a["Webkit"+e]="webkit"+l,a["Moz"+e]="moz"+l,a}var Ia={animationend:Ea("Animation","AnimationEnd"),animationiteration:Ea("Animation","AnimationIteration"),animationstart:Ea("Animation","AnimationStart"),transitionrun:Ea("Transition","TransitionRun"),transitionstart:Ea("Transition","TransitionStart"),transitioncancel:Ea("Transition","TransitionCancel"),transitionend:Ea("Transition","TransitionEnd")},yc={},ur={};Bl&&(ur=document.createElement("div").style,"AnimationEvent"in window||(delete Ia.animationend.animation,delete Ia.animationiteration.animation,delete Ia.animationstart.animation),"TransitionEvent"in window||delete Ia.transitionend.transition);function Aa(e){if(yc[e])return yc[e];if(!Ia[e])return e;var l=Ia[e],a;for(a in l)if(l.hasOwnProperty(a)&&a in ur)return yc[e]=l[a];return e}var sr=Aa("animationend"),rr=Aa("animationiteration"),fr=Aa("animationstart"),Cm=Aa("transitionrun"),Rm=Aa("transitionstart"),Hm=Aa("transitioncancel"),or=Aa("transitionend"),dr=new Map,bc="abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(" ");bc.push("scrollEnd");function El(e,l){dr.set(e,l),za(l,[e])}var Yn=typeof reportError=="function"?reportError:function(e){if(typeof window=="object"&&typeof window.ErrorEvent=="function"){var l=new window.ErrorEvent("error",{bubbles:!0,cancelable:!0,message:typeof e=="object"&&e!==null&&typeof e.message=="string"?String(e.message):String(e),error:e});if(!window.dispatchEvent(l))return}else if(typeof process=="object"&&typeof process.emit=="function"){process.emit("uncaughtException",e);return}console.error(e)},yl=[],et=0,xc=0;function Gn(){for(var e=et,l=xc=et=0;l<e;){var a=yl[l];yl[l++]=null;var t=yl[l];yl[l++]=null;var n=yl[l];yl[l++]=null;var i=yl[l];if(yl[l++]=null,t!==null&&n!==null){var u=t.pending;u===null?n.next=n:(n.next=u.next,u.next=n),t.pending=n}i!==0&&mr(a,n,i)}}function Xn(e,l,a,t){yl[et++]=e,yl[et++]=l,yl[et++]=a,yl[et++]=t,xc|=t,e.lanes|=t,e=e.alternate,e!==null&&(e.lanes|=t)}function jc(e,l,a,t){return Xn(e,l,a,t),Qn(e)}function Oa(e,l){return Xn(e,null,null,l),Qn(e)}function mr(e,l,a){e.lanes|=a;var t=e.alternate;t!==null&&(t.lanes|=a);for(var n=!1,i=e.return;i!==null;)i.childLanes|=a,t=i.alternate,t!==null&&(t.childLanes|=a),i.tag===22&&(e=i.stateNode,e===null||e._visibility&1||(n=!0)),e=i,i=i.return;return e.tag===3?(i=e.stateNode,n&&l!==null&&(n=31-sl(a),e=i.hiddenUpdates,t=e[n],t===null?e[n]=[l]:t.push(l),l.lane=a|536870912),i):null}function Qn(e){if(50<rn)throw rn=0,Du=null,Error(r(185));for(var l=e.return;l!==null;)e=l,l=e.return;return e.tag===3?e.stateNode:null}var lt={};function Bm(e,l,a,t){this.tag=e,this.key=a,this.sibling=this.child=this.return=this.stateNode=this.type=this.elementType=null,this.index=0,this.refCleanup=this.ref=null,this.pendingProps=l,this.dependencies=this.memoizedState=this.updateQueue=this.memoizedProps=null,this.mode=t,this.subtreeFlags=this.flags=0,this.deletions=null,this.childLanes=this.lanes=0,this.alternate=null}function fl(e,l,a,t){return new Bm(e,l,a,t)}function Sc(e){return e=e.prototype,!(!e||!e.isReactComponent)}function ql(e,l){var a=e.alternate;return a===null?(a=fl(e.tag,l,e.key,e.mode),a.elementType=e.elementType,a.type=e.type,a.stateNode=e.stateNode,a.alternate=e,e.alternate=a):(a.pendingProps=l,a.type=e.type,a.flags=0,a.subtreeFlags=0,a.deletions=null),a.flags=e.flags&65011712,a.childLanes=e.childLanes,a.lanes=e.lanes,a.child=e.child,a.memoizedProps=e.memoizedProps,a.memoizedState=e.memoizedState,a.updateQueue=e.updateQueue,l=e.dependencies,a.dependencies=l===null?null:{lanes:l.lanes,firstContext:l.firstContext},a.sibling=e.sibling,a.index=e.index,a.ref=e.ref,a.refCleanup=e.refCleanup,a}function hr(e,l){e.flags&=65011714;var a=e.alternate;return a===null?(e.childLanes=0,e.lanes=l,e.child=null,e.subtreeFlags=0,e.memoizedProps=null,e.memoizedState=null,e.updateQueue=null,e.dependencies=null,e.stateNode=null):(e.childLanes=a.childLanes,e.lanes=a.lanes,e.child=a.child,e.subtreeFlags=0,e.deletions=null,e.memoizedProps=a.memoizedProps,e.memoizedState=a.memoizedState,e.updateQueue=a.updateQueue,e.type=a.type,l=a.dependencies,e.dependencies=l===null?null:{lanes:l.lanes,firstContext:l.firstContext}),e}function Ln(e,l,a,t,n,i){var u=0;if(t=e,typeof e=="function")Sc(e)&&(u=1);else if(typeof e=="string")u=Qh(e,a,M.current)?26:e==="html"||e==="head"||e==="body"?27:5;else e:switch(e){case $e:return e=fl(31,a,l,n),e.elementType=$e,e.lanes=i,e;case _e:return Da(a.children,n,i,l);case tl:u=8,n|=24;break;case q:return e=fl(12,a,l,n|2),e.elementType=q,e.lanes=i,e;case nl:return e=fl(13,a,l,n),e.elementType=nl,e.lanes=i,e;case qe:return e=fl(19,a,l,n),e.elementType=qe,e.lanes=i,e;default:if(typeof e=="object"&&e!==null)switch(e.$$typeof){case ve:u=10;break e;case be:u=9;break e;case ke:u=11;break e;case P:u=14;break e;case je:u=16,t=null;break e}u=29,a=Error(r(130,e===null?"null":typeof e,"")),t=null}return l=fl(u,a,l,n),l.elementType=e,l.type=t,l.lanes=i,l}function Da(e,l,a,t){return e=fl(7,e,t,l),e.lanes=a,e}function Nc(e,l,a){return e=fl(6,e,null,l),e.lanes=a,e}function pr(e){var l=fl(18,null,null,0);return l.stateNode=e,l}function _c(e,l,a){return l=fl(4,e.children!==null?e.children:[],e.key,l),l.lanes=a,l.stateNode={containerInfo:e.containerInfo,pendingChildren:null,implementation:e.implementation},l}var vr=new WeakMap;function bl(e,l){if(typeof e=="object"&&e!==null){var a=vr.get(e);return a!==void 0?a:(l={value:e,source:l,stack:ps(l)},vr.set(e,l),l)}return{value:e,source:l,stack:ps(l)}}var at=[],tt=0,Zn=null,Qt=0,xl=[],jl=0,la=null,Dl=1,Ml="";function Yl(e,l){at[tt++]=Qt,at[tt++]=Zn,Zn=e,Qt=l}function gr(e,l,a){xl[jl++]=Dl,xl[jl++]=Ml,xl[jl++]=la,la=e;var t=Dl;e=Ml;var n=32-sl(t)-1;t&=~(1<<n),a+=1;var i=32-sl(l)+n;if(30<i){var u=n-n%5;i=(t&(1<<u)-1).toString(32),t>>=u,n-=u,Dl=1<<32-sl(l)+n|a<<n|t,Ml=i+e}else Dl=1<<i|a<<n|t,Ml=e}function zc(e){e.return!==null&&(Yl(e,1),gr(e,1,0))}function Tc(e){for(;e===Zn;)Zn=at[--tt],at[tt]=null,Qt=at[--tt],at[tt]=null;for(;e===la;)la=xl[--jl],xl[jl]=null,Ml=xl[--jl],xl[jl]=null,Dl=xl[--jl],xl[jl]=null}function yr(e,l){xl[jl++]=Dl,xl[jl++]=Ml,xl[jl++]=la,Dl=l.id,Ml=l.overflow,la=e}var Xe=null,ge=null,te=!1,aa=null,Sl=!1,Ec=Error(r(519));function ta(e){var l=Error(r(418,1<arguments.length&&arguments[1]!==void 0&&arguments[1]?"text":"HTML",""));throw Lt(bl(l,e)),Ec}function br(e){var l=e.stateNode,a=e.type,t=e.memoizedProps;switch(l[Ge]=e,l[We]=t,a){case"dialog":ee("cancel",l),ee("close",l);break;case"iframe":case"object":case"embed":ee("load",l);break;case"video":case"audio":for(a=0;a<on.length;a++)ee(on[a],l);break;case"source":ee("error",l);break;case"img":case"image":case"link":ee("error",l),ee("load",l);break;case"details":ee("toggle",l);break;case"input":ee("invalid",l),Us(l,t.value,t.defaultValue,t.checked,t.defaultChecked,t.type,t.name,!0);break;case"select":ee("invalid",l);break;case"textarea":ee("invalid",l),Rs(l,t.value,t.defaultValue,t.children)}a=t.children,typeof a!="string"&&typeof a!="number"&&typeof a!="bigint"||l.textContent===""+a||t.suppressHydrationWarning===!0||Yo(l.textContent,a)?(t.popover!=null&&(ee("beforetoggle",l),ee("toggle",l)),t.onScroll!=null&&ee("scroll",l),t.onScrollEnd!=null&&ee("scrollend",l),t.onClick!=null&&(l.onclick=Hl),l=!0):l=!1,l||ta(e,!0)}function xr(e){for(Xe=e.return;Xe;)switch(Xe.tag){case 5:case 31:case 13:Sl=!1;return;case 27:case 3:Sl=!0;return;default:Xe=Xe.return}}function nt(e){if(e!==Xe)return!1;if(!te)return xr(e),te=!0,!1;var l=e.tag,a;if((a=l!==3&&l!==27)&&((a=l===5)&&(a=e.type,a=!(a!=="form"&&a!=="button")||Vu(e.type,e.memoizedProps)),a=!a),a&&ge&&ta(e),xr(e),l===13){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(r(317));ge=Ko(e)}else if(l===31){if(e=e.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(r(317));ge=Ko(e)}else l===27?(l=ge,ga(e.type)?(e=Wu,Wu=null,ge=e):ge=l):ge=Xe?_l(e.stateNode.nextSibling):null;return!0}function Ma(){ge=Xe=null,te=!1}function Ac(){var e=aa;return e!==null&&(ll===null?ll=e:ll.push.apply(ll,e),aa=null),e}function Lt(e){aa===null?aa=[e]:aa.push(e)}var Oc=d(null),Ua=null,Gl=null;function na(e,l,a){C(Oc,l._currentValue),l._currentValue=a}function Xl(e){e._currentValue=Oc.current,T(Oc)}function Dc(e,l,a){for(;e!==null;){var t=e.alternate;if((e.childLanes&l)!==l?(e.childLanes|=l,t!==null&&(t.childLanes|=l)):t!==null&&(t.childLanes&l)!==l&&(t.childLanes|=l),e===a)break;e=e.return}}function Mc(e,l,a,t){var n=e.child;for(n!==null&&(n.return=e);n!==null;){var i=n.dependencies;if(i!==null){var u=n.child;i=i.firstContext;e:for(;i!==null;){var s=i;i=n;for(var f=0;f<l.length;f++)if(s.context===l[f]){i.lanes|=a,s=i.alternate,s!==null&&(s.lanes|=a),Dc(i.return,a,e),t||(u=null);break e}i=s.next}}else if(n.tag===18){if(u=n.return,u===null)throw Error(r(341));u.lanes|=a,i=u.alternate,i!==null&&(i.lanes|=a),Dc(u,a,e),u=null}else u=n.child;if(u!==null)u.return=n;else for(u=n;u!==null;){if(u===e){u=null;break}if(n=u.sibling,n!==null){n.return=u.return,u=n;break}u=u.return}n=u}}function it(e,l,a,t){e=null;for(var n=l,i=!1;n!==null;){if(!i){if((n.flags&524288)!==0)i=!0;else if((n.flags&262144)!==0)break}if(n.tag===10){var u=n.alternate;if(u===null)throw Error(r(387));if(u=u.memoizedProps,u!==null){var s=n.type;rl(n.pendingProps.value,u.value)||(e!==null?e.push(s):e=[s])}}else if(n===J.current){if(u=n.alternate,u===null)throw Error(r(387));u.memoizedState.memoizedState!==n.memoizedState.memoizedState&&(e!==null?e.push(vn):e=[vn])}n=n.return}e!==null&&Mc(l,e,a,t),l.flags|=262144}function wn(e){for(e=e.firstContext;e!==null;){if(!rl(e.context._currentValue,e.memoizedValue))return!0;e=e.next}return!1}function Ca(e){Ua=e,Gl=null,e=e.dependencies,e!==null&&(e.firstContext=null)}function Qe(e){return jr(Ua,e)}function Vn(e,l){return Ua===null&&Ca(e),jr(e,l)}function jr(e,l){var a=l._currentValue;if(l={context:l,memoizedValue:a,next:null},Gl===null){if(e===null)throw Error(r(308));Gl=l,e.dependencies={lanes:0,firstContext:l},e.flags|=524288}else Gl=Gl.next=l;return a}var qm=typeof AbortController<"u"?AbortController:function(){var e=[],l=this.signal={aborted:!1,addEventListener:function(a,t){e.push(t)}};this.abort=function(){l.aborted=!0,e.forEach(function(a){return a()})}},Ym=j.unstable_scheduleCallback,Gm=j.unstable_NormalPriority,Ae={$$typeof:ve,Consumer:null,Provider:null,_currentValue:null,_currentValue2:null,_threadCount:0};function Uc(){return{controller:new qm,data:new Map,refCount:0}}function Zt(e){e.refCount--,e.refCount===0&&Ym(Gm,function(){e.controller.abort()})}var wt=null,Cc=0,ct=0,ut=null;function Xm(e,l){if(wt===null){var a=wt=[];Cc=0,ct=Bu(),ut={status:"pending",value:void 0,then:function(t){a.push(t)}}}return Cc++,l.then(Sr,Sr),l}function Sr(){if(--Cc===0&&wt!==null){ut!==null&&(ut.status="fulfilled");var e=wt;wt=null,ct=0,ut=null;for(var l=0;l<e.length;l++)(0,e[l])()}}function Qm(e,l){var a=[],t={status:"pending",value:null,reason:null,then:function(n){a.push(n)}};return e.then(function(){t.status="fulfilled",t.value=l;for(var n=0;n<a.length;n++)(0,a[n])(l)},function(n){for(t.status="rejected",t.reason=n,n=0;n<a.length;n++)(0,a[n])(void 0)}),t}var Nr=N.S;N.S=function(e,l){uo=cl(),typeof l=="object"&&l!==null&&typeof l.then=="function"&&Xm(e,l),Nr!==null&&Nr(e,l)};var Ra=d(null);function Rc(){var e=Ra.current;return e!==null?e:pe.pooledCache}function kn(e,l){l===null?C(Ra,Ra.current):C(Ra,l.pool)}function _r(){var e=Rc();return e===null?null:{parent:Ae._currentValue,pool:e}}var st=Error(r(460)),Hc=Error(r(474)),Kn=Error(r(542)),Jn={then:function(){}};function zr(e){return e=e.status,e==="fulfilled"||e==="rejected"}function Tr(e,l,a){switch(a=e[a],a===void 0?e.push(l):a!==l&&(l.then(Hl,Hl),l=a),l.status){case"fulfilled":return l.value;case"rejected":throw e=l.reason,Ar(e),e;default:if(typeof l.status=="string")l.then(Hl,Hl);else{if(e=pe,e!==null&&100<e.shellSuspendCounter)throw Error(r(482));e=l,e.status="pending",e.then(function(t){if(l.status==="pending"){var n=l;n.status="fulfilled",n.value=t}},function(t){if(l.status==="pending"){var n=l;n.status="rejected",n.reason=t}})}switch(l.status){case"fulfilled":return l.value;case"rejected":throw e=l.reason,Ar(e),e}throw Ba=l,st}}function Ha(e){try{var l=e._init;return l(e._payload)}catch(a){throw a!==null&&typeof a=="object"&&typeof a.then=="function"?(Ba=a,st):a}}var Ba=null;function Er(){if(Ba===null)throw Error(r(459));var e=Ba;return Ba=null,e}function Ar(e){if(e===st||e===Kn)throw Error(r(483))}var rt=null,Vt=0;function $n(e){var l=Vt;return Vt+=1,rt===null&&(rt=[]),Tr(rt,e,l)}function kt(e,l){l=l.props.ref,e.ref=l!==void 0?l:null}function Wn(e,l){throw l.$$typeof===W?Error(r(525)):(e=Object.prototype.toString.call(l),Error(r(31,e==="[object Object]"?"object with keys {"+Object.keys(l).join(", ")+"}":e)))}function Or(e){function l(m,o){if(e){var p=m.deletions;p===null?(m.deletions=[o],m.flags|=16):p.push(o)}}function a(m,o){if(!e)return null;for(;o!==null;)l(m,o),o=o.sibling;return null}function t(m){for(var o=new Map;m!==null;)m.key!==null?o.set(m.key,m):o.set(m.index,m),m=m.sibling;return o}function n(m,o){return m=ql(m,o),m.index=0,m.sibling=null,m}function i(m,o,p){return m.index=p,e?(p=m.alternate,p!==null?(p=p.index,p<o?(m.flags|=67108866,o):p):(m.flags|=67108866,o)):(m.flags|=1048576,o)}function u(m){return e&&m.alternate===null&&(m.flags|=67108866),m}function s(m,o,p,_){return o===null||o.tag!==6?(o=Nc(p,m.mode,_),o.return=m,o):(o=n(o,p),o.return=m,o)}function f(m,o,p,_){var Z=p.type;return Z===_e?S(m,o,p.props.children,_,p.key):o!==null&&(o.elementType===Z||typeof Z=="object"&&Z!==null&&Z.$$typeof===je&&Ha(Z)===o.type)?(o=n(o,p.props),kt(o,p),o.return=m,o):(o=Ln(p.type,p.key,p.props,null,m.mode,_),kt(o,p),o.return=m,o)}function v(m,o,p,_){return o===null||o.tag!==4||o.stateNode.containerInfo!==p.containerInfo||o.stateNode.implementation!==p.implementation?(o=_c(p,m.mode,_),o.return=m,o):(o=n(o,p.children||[]),o.return=m,o)}function S(m,o,p,_,Z){return o===null||o.tag!==7?(o=Da(p,m.mode,_,Z),o.return=m,o):(o=n(o,p),o.return=m,o)}function z(m,o,p){if(typeof o=="string"&&o!==""||typeof o=="number"||typeof o=="bigint")return o=Nc(""+o,m.mode,p),o.return=m,o;if(typeof o=="object"&&o!==null){switch(o.$$typeof){case U:return p=Ln(o.type,o.key,o.props,null,m.mode,p),kt(p,o),p.return=m,p;case se:return o=_c(o,m.mode,p),o.return=m,o;case je:return o=Ha(o),z(m,o,p)}if(il(o)||Re(o))return o=Da(o,m.mode,p,null),o.return=m,o;if(typeof o.then=="function")return z(m,$n(o),p);if(o.$$typeof===ve)return z(m,Vn(m,o),p);Wn(m,o)}return null}function g(m,o,p,_){var Z=o!==null?o.key:null;if(typeof p=="string"&&p!==""||typeof p=="number"||typeof p=="bigint")return Z!==null?null:s(m,o,""+p,_);if(typeof p=="object"&&p!==null){switch(p.$$typeof){case U:return p.key===Z?f(m,o,p,_):null;case se:return p.key===Z?v(m,o,p,_):null;case je:return p=Ha(p),g(m,o,p,_)}if(il(p)||Re(p))return Z!==null?null:S(m,o,p,_,null);if(typeof p.then=="function")return g(m,o,$n(p),_);if(p.$$typeof===ve)return g(m,o,Vn(m,p),_);Wn(m,p)}return null}function x(m,o,p,_,Z){if(typeof _=="string"&&_!==""||typeof _=="number"||typeof _=="bigint")return m=m.get(p)||null,s(o,m,""+_,Z);if(typeof _=="object"&&_!==null){switch(_.$$typeof){case U:return m=m.get(_.key===null?p:_.key)||null,f(o,m,_,Z);case se:return m=m.get(_.key===null?p:_.key)||null,v(o,m,_,Z);case je:return _=Ha(_),x(m,o,p,_,Z)}if(il(_)||Re(_))return m=m.get(p)||null,S(o,m,_,Z,null);if(typeof _.then=="function")return x(m,o,p,$n(_),Z);if(_.$$typeof===ve)return x(m,o,p,Vn(o,_),Z);Wn(o,_)}return null}function Y(m,o,p,_){for(var Z=null,ne=null,Q=o,F=o=0,ae=null;Q!==null&&F<p.length;F++){Q.index>F?(ae=Q,Q=null):ae=Q.sibling;var ie=g(m,Q,p[F],_);if(ie===null){Q===null&&(Q=ae);break}e&&Q&&ie.alternate===null&&l(m,Q),o=i(ie,o,F),ne===null?Z=ie:ne.sibling=ie,ne=ie,Q=ae}if(F===p.length)return a(m,Q),te&&Yl(m,F),Z;if(Q===null){for(;F<p.length;F++)Q=z(m,p[F],_),Q!==null&&(o=i(Q,o,F),ne===null?Z=Q:ne.sibling=Q,ne=Q);return te&&Yl(m,F),Z}for(Q=t(Q);F<p.length;F++)ae=x(Q,m,F,p[F],_),ae!==null&&(e&&ae.alternate!==null&&Q.delete(ae.key===null?F:ae.key),o=i(ae,o,F),ne===null?Z=ae:ne.sibling=ae,ne=ae);return e&&Q.forEach(function(Sa){return l(m,Sa)}),te&&Yl(m,F),Z}function V(m,o,p,_){if(p==null)throw Error(r(151));for(var Z=null,ne=null,Q=o,F=o=0,ae=null,ie=p.next();Q!==null&&!ie.done;F++,ie=p.next()){Q.index>F?(ae=Q,Q=null):ae=Q.sibling;var Sa=g(m,Q,ie.value,_);if(Sa===null){Q===null&&(Q=ae);break}e&&Q&&Sa.alternate===null&&l(m,Q),o=i(Sa,o,F),ne===null?Z=Sa:ne.sibling=Sa,ne=Sa,Q=ae}if(ie.done)return a(m,Q),te&&Yl(m,F),Z;if(Q===null){for(;!ie.done;F++,ie=p.next())ie=z(m,ie.value,_),ie!==null&&(o=i(ie,o,F),ne===null?Z=ie:ne.sibling=ie,ne=ie);return te&&Yl(m,F),Z}for(Q=t(Q);!ie.done;F++,ie=p.next())ie=x(Q,m,F,ie.value,_),ie!==null&&(e&&ie.alternate!==null&&Q.delete(ie.key===null?F:ie.key),o=i(ie,o,F),ne===null?Z=ie:ne.sibling=ie,ne=ie);return e&&Q.forEach(function(Ph){return l(m,Ph)}),te&&Yl(m,F),Z}function he(m,o,p,_){if(typeof p=="object"&&p!==null&&p.type===_e&&p.key===null&&(p=p.props.children),typeof p=="object"&&p!==null){switch(p.$$typeof){case U:e:{for(var Z=p.key;o!==null;){if(o.key===Z){if(Z=p.type,Z===_e){if(o.tag===7){a(m,o.sibling),_=n(o,p.props.children),_.return=m,m=_;break e}}else if(o.elementType===Z||typeof Z=="object"&&Z!==null&&Z.$$typeof===je&&Ha(Z)===o.type){a(m,o.sibling),_=n(o,p.props),kt(_,p),_.return=m,m=_;break e}a(m,o);break}else l(m,o);o=o.sibling}p.type===_e?(_=Da(p.props.children,m.mode,_,p.key),_.return=m,m=_):(_=Ln(p.type,p.key,p.props,null,m.mode,_),kt(_,p),_.return=m,m=_)}return u(m);case se:e:{for(Z=p.key;o!==null;){if(o.key===Z)if(o.tag===4&&o.stateNode.containerInfo===p.containerInfo&&o.stateNode.implementation===p.implementation){a(m,o.sibling),_=n(o,p.children||[]),_.return=m,m=_;break e}else{a(m,o);break}else l(m,o);o=o.sibling}_=_c(p,m.mode,_),_.return=m,m=_}return u(m);case je:return p=Ha(p),he(m,o,p,_)}if(il(p))return Y(m,o,p,_);if(Re(p)){if(Z=Re(p),typeof Z!="function")throw Error(r(150));return p=Z.call(p),V(m,o,p,_)}if(typeof p.then=="function")return he(m,o,$n(p),_);if(p.$$typeof===ve)return he(m,o,Vn(m,p),_);Wn(m,p)}return typeof p=="string"&&p!==""||typeof p=="number"||typeof p=="bigint"?(p=""+p,o!==null&&o.tag===6?(a(m,o.sibling),_=n(o,p),_.return=m,m=_):(a(m,o),_=Nc(p,m.mode,_),_.return=m,m=_),u(m)):a(m,o)}return function(m,o,p,_){try{Vt=0;var Z=he(m,o,p,_);return rt=null,Z}catch(Q){if(Q===st||Q===Kn)throw Q;var ne=fl(29,Q,null,m.mode);return ne.lanes=_,ne.return=m,ne}}}var qa=Or(!0),Dr=Or(!1),ia=!1;function Bc(e){e.updateQueue={baseState:e.memoizedState,firstBaseUpdate:null,lastBaseUpdate:null,shared:{pending:null,lanes:0,hiddenCallbacks:null},callbacks:null}}function qc(e,l){e=e.updateQueue,l.updateQueue===e&&(l.updateQueue={baseState:e.baseState,firstBaseUpdate:e.firstBaseUpdate,lastBaseUpdate:e.lastBaseUpdate,shared:e.shared,callbacks:null})}function ca(e){return{lane:e,tag:0,payload:null,callback:null,next:null}}function ua(e,l,a){var t=e.updateQueue;if(t===null)return null;if(t=t.shared,(ce&2)!==0){var n=t.pending;return n===null?l.next=l:(l.next=n.next,n.next=l),t.pending=l,l=Qn(e),mr(e,null,a),l}return Xn(e,t,l,a),Qn(e)}function Kt(e,l,a){if(l=l.updateQueue,l!==null&&(l=l.shared,(a&4194048)!==0)){var t=l.lanes;t&=e.pendingLanes,a|=t,l.lanes=a,js(e,a)}}function Yc(e,l){var a=e.updateQueue,t=e.alternate;if(t!==null&&(t=t.updateQueue,a===t)){var n=null,i=null;if(a=a.firstBaseUpdate,a!==null){do{var u={lane:a.lane,tag:a.tag,payload:a.payload,callback:null,next:null};i===null?n=i=u:i=i.next=u,a=a.next}while(a!==null);i===null?n=i=l:i=i.next=l}else n=i=l;a={baseState:t.baseState,firstBaseUpdate:n,lastBaseUpdate:i,shared:t.shared,callbacks:t.callbacks},e.updateQueue=a;return}e=a.lastBaseUpdate,e===null?a.firstBaseUpdate=l:e.next=l,a.lastBaseUpdate=l}var Gc=!1;function Jt(){if(Gc){var e=ut;if(e!==null)throw e}}function $t(e,l,a,t){Gc=!1;var n=e.updateQueue;ia=!1;var i=n.firstBaseUpdate,u=n.lastBaseUpdate,s=n.shared.pending;if(s!==null){n.shared.pending=null;var f=s,v=f.next;f.next=null,u===null?i=v:u.next=v,u=f;var S=e.alternate;S!==null&&(S=S.updateQueue,s=S.lastBaseUpdate,s!==u&&(s===null?S.firstBaseUpdate=v:s.next=v,S.lastBaseUpdate=f))}if(i!==null){var z=n.baseState;u=0,S=v=f=null,s=i;do{var g=s.lane&-536870913,x=g!==s.lane;if(x?(le&g)===g:(t&g)===g){g!==0&&g===ct&&(Gc=!0),S!==null&&(S=S.next={lane:0,tag:s.tag,payload:s.payload,callback:null,next:null});e:{var Y=e,V=s;g=l;var he=a;switch(V.tag){case 1:if(Y=V.payload,typeof Y=="function"){z=Y.call(he,z,g);break e}z=Y;break e;case 3:Y.flags=Y.flags&-65537|128;case 0:if(Y=V.payload,g=typeof Y=="function"?Y.call(he,z,g):Y,g==null)break e;z=A({},z,g);break e;case 2:ia=!0}}g=s.callback,g!==null&&(e.flags|=64,x&&(e.flags|=8192),x=n.callbacks,x===null?n.callbacks=[g]:x.push(g))}else x={lane:g,tag:s.tag,payload:s.payload,callback:s.callback,next:null},S===null?(v=S=x,f=z):S=S.next=x,u|=g;if(s=s.next,s===null){if(s=n.shared.pending,s===null)break;x=s,s=x.next,x.next=null,n.lastBaseUpdate=x,n.shared.pending=null}}while(!0);S===null&&(f=z),n.baseState=f,n.firstBaseUpdate=v,n.lastBaseUpdate=S,i===null&&(n.shared.lanes=0),da|=u,e.lanes=u,e.memoizedState=z}}function Mr(e,l){if(typeof e!="function")throw Error(r(191,e));e.call(l)}function Ur(e,l){var a=e.callbacks;if(a!==null)for(e.callbacks=null,e=0;e<a.length;e++)Mr(a[e],l)}var ft=d(null),Fn=d(0);function Cr(e,l){e=$l,C(Fn,e),C(ft,l),$l=e|l.baseLanes}function Xc(){C(Fn,$l),C(ft,ft.current)}function Qc(){$l=Fn.current,T(ft),T(Fn)}var ol=d(null),Nl=null;function sa(e){var l=e.alternate;C(Te,Te.current&1),C(ol,e),Nl===null&&(l===null||ft.current!==null||l.memoizedState!==null)&&(Nl=e)}function Lc(e){C(Te,Te.current),C(ol,e),Nl===null&&(Nl=e)}function Rr(e){e.tag===22?(C(Te,Te.current),C(ol,e),Nl===null&&(Nl=e)):ra()}function ra(){C(Te,Te.current),C(ol,ol.current)}function dl(e){T(ol),Nl===e&&(Nl=null),T(Te)}var Te=d(0);function Pn(e){for(var l=e;l!==null;){if(l.tag===13){var a=l.memoizedState;if(a!==null&&(a=a.dehydrated,a===null||Ju(a)||$u(a)))return l}else if(l.tag===19&&(l.memoizedProps.revealOrder==="forwards"||l.memoizedProps.revealOrder==="backwards"||l.memoizedProps.revealOrder==="unstable_legacy-backwards"||l.memoizedProps.revealOrder==="together")){if((l.flags&128)!==0)return l}else if(l.child!==null){l.child.return=l,l=l.child;continue}if(l===e)break;for(;l.sibling===null;){if(l.return===null||l.return===e)return null;l=l.return}l.sibling.return=l.return,l=l.sibling}return null}var Ql=0,$=null,de=null,Oe=null,In=!1,ot=!1,Ya=!1,ei=0,Wt=0,dt=null,Lm=0;function Se(){throw Error(r(321))}function Zc(e,l){if(l===null)return!1;for(var a=0;a<l.length&&a<e.length;a++)if(!rl(e[a],l[a]))return!1;return!0}function wc(e,l,a,t,n,i){return Ql=i,$=l,l.memoizedState=null,l.updateQueue=null,l.lanes=0,N.H=e===null||e.memoizedState===null?yf:iu,Ya=!1,i=a(t,n),Ya=!1,ot&&(i=Br(l,a,t,n)),Hr(e),i}function Hr(e){N.H=It;var l=de!==null&&de.next!==null;if(Ql=0,Oe=de=$=null,In=!1,Wt=0,dt=null,l)throw Error(r(300));e===null||De||(e=e.dependencies,e!==null&&wn(e)&&(De=!0))}function Br(e,l,a,t){$=e;var n=0;do{if(ot&&(dt=null),Wt=0,ot=!1,25<=n)throw Error(r(301));if(n+=1,Oe=de=null,e.updateQueue!=null){var i=e.updateQueue;i.lastEffect=null,i.events=null,i.stores=null,i.memoCache!=null&&(i.memoCache.index=0)}N.H=bf,i=l(a,t)}while(ot);return i}function Zm(){var e=N.H,l=e.useState()[0];return l=typeof l.then=="function"?Ft(l):l,e=e.useState()[0],(de!==null?de.memoizedState:null)!==e&&($.flags|=1024),l}function Vc(){var e=ei!==0;return ei=0,e}function kc(e,l,a){l.updateQueue=e.updateQueue,l.flags&=-2053,e.lanes&=~a}function Kc(e){if(In){for(e=e.memoizedState;e!==null;){var l=e.queue;l!==null&&(l.pending=null),e=e.next}In=!1}Ql=0,Oe=de=$=null,ot=!1,Wt=ei=0,dt=null}function Je(){var e={memoizedState:null,baseState:null,baseQueue:null,queue:null,next:null};return Oe===null?$.memoizedState=Oe=e:Oe=Oe.next=e,Oe}function Ee(){if(de===null){var e=$.alternate;e=e!==null?e.memoizedState:null}else e=de.next;var l=Oe===null?$.memoizedState:Oe.next;if(l!==null)Oe=l,de=e;else{if(e===null)throw $.alternate===null?Error(r(467)):Error(r(310));de=e,e={memoizedState:de.memoizedState,baseState:de.baseState,baseQueue:de.baseQueue,queue:de.queue,next:null},Oe===null?$.memoizedState=Oe=e:Oe=Oe.next=e}return Oe}function li(){return{lastEffect:null,events:null,stores:null,memoCache:null}}function Ft(e){var l=Wt;return Wt+=1,dt===null&&(dt=[]),e=Tr(dt,e,l),l=$,(Oe===null?l.memoizedState:Oe.next)===null&&(l=l.alternate,N.H=l===null||l.memoizedState===null?yf:iu),e}function ai(e){if(e!==null&&typeof e=="object"){if(typeof e.then=="function")return Ft(e);if(e.$$typeof===ve)return Qe(e)}throw Error(r(438,String(e)))}function Jc(e){var l=null,a=$.updateQueue;if(a!==null&&(l=a.memoCache),l==null){var t=$.alternate;t!==null&&(t=t.updateQueue,t!==null&&(t=t.memoCache,t!=null&&(l={data:t.data.map(function(n){return n.slice()}),index:0})))}if(l==null&&(l={data:[],index:0}),a===null&&(a=li(),$.updateQueue=a),a.memoCache=l,a=l.data[l.index],a===void 0)for(a=l.data[l.index]=Array(e),t=0;t<e;t++)a[t]=Ue;return l.index++,a}function Ll(e,l){return typeof l=="function"?l(e):l}function ti(e){var l=Ee();return $c(l,de,e)}function $c(e,l,a){var t=e.queue;if(t===null)throw Error(r(311));t.lastRenderedReducer=a;var n=e.baseQueue,i=t.pending;if(i!==null){if(n!==null){var u=n.next;n.next=i.next,i.next=u}l.baseQueue=n=i,t.pending=null}if(i=e.baseState,n===null)e.memoizedState=i;else{l=n.next;var s=u=null,f=null,v=l,S=!1;do{var z=v.lane&-536870913;if(z!==v.lane?(le&z)===z:(Ql&z)===z){var g=v.revertLane;if(g===0)f!==null&&(f=f.next={lane:0,revertLane:0,gesture:null,action:v.action,hasEagerState:v.hasEagerState,eagerState:v.eagerState,next:null}),z===ct&&(S=!0);else if((Ql&g)===g){v=v.next,g===ct&&(S=!0);continue}else z={lane:0,revertLane:v.revertLane,gesture:null,action:v.action,hasEagerState:v.hasEagerState,eagerState:v.eagerState,next:null},f===null?(s=f=z,u=i):f=f.next=z,$.lanes|=g,da|=g;z=v.action,Ya&&a(i,z),i=v.hasEagerState?v.eagerState:a(i,z)}else g={lane:z,revertLane:v.revertLane,gesture:v.gesture,action:v.action,hasEagerState:v.hasEagerState,eagerState:v.eagerState,next:null},f===null?(s=f=g,u=i):f=f.next=g,$.lanes|=z,da|=z;v=v.next}while(v!==null&&v!==l);if(f===null?u=i:f.next=s,!rl(i,e.memoizedState)&&(De=!0,S&&(a=ut,a!==null)))throw a;e.memoizedState=i,e.baseState=u,e.baseQueue=f,t.lastRenderedState=i}return n===null&&(t.lanes=0),[e.memoizedState,t.dispatch]}function Wc(e){var l=Ee(),a=l.queue;if(a===null)throw Error(r(311));a.lastRenderedReducer=e;var t=a.dispatch,n=a.pending,i=l.memoizedState;if(n!==null){a.pending=null;var u=n=n.next;do i=e(i,u.action),u=u.next;while(u!==n);rl(i,l.memoizedState)||(De=!0),l.memoizedState=i,l.baseQueue===null&&(l.baseState=i),a.lastRenderedState=i}return[i,t]}function qr(e,l,a){var t=$,n=Ee(),i=te;if(i){if(a===void 0)throw Error(r(407));a=a()}else a=l();var u=!rl((de||n).memoizedState,a);if(u&&(n.memoizedState=a,De=!0),n=n.queue,Ic(Xr.bind(null,t,n,e),[e]),n.getSnapshot!==l||u||Oe!==null&&Oe.memoizedState.tag&1){if(t.flags|=2048,mt(9,{destroy:void 0},Gr.bind(null,t,n,a,l),null),pe===null)throw Error(r(349));i||(Ql&127)!==0||Yr(t,l,a)}return a}function Yr(e,l,a){e.flags|=16384,e={getSnapshot:l,value:a},l=$.updateQueue,l===null?(l=li(),$.updateQueue=l,l.stores=[e]):(a=l.stores,a===null?l.stores=[e]:a.push(e))}function Gr(e,l,a,t){l.value=a,l.getSnapshot=t,Qr(l)&&Lr(e)}function Xr(e,l,a){return a(function(){Qr(l)&&Lr(e)})}function Qr(e){var l=e.getSnapshot;e=e.value;try{var a=l();return!rl(e,a)}catch{return!0}}function Lr(e){var l=Oa(e,2);l!==null&&al(l,e,2)}function Fc(e){var l=Je();if(typeof e=="function"){var a=e;if(e=a(),Ya){Pl(!0);try{a()}finally{Pl(!1)}}}return l.memoizedState=l.baseState=e,l.queue={pending:null,lanes:0,dispatch:null,lastRenderedReducer:Ll,lastRenderedState:e},l}function Zr(e,l,a,t){return e.baseState=a,$c(e,de,typeof t=="function"?t:Ll)}function wm(e,l,a,t,n){if(ci(e))throw Error(r(485));if(e=l.action,e!==null){var i={payload:n,action:e,next:null,isTransition:!0,status:"pending",value:null,reason:null,listeners:[],then:function(u){i.listeners.push(u)}};N.T!==null?a(!0):i.isTransition=!1,t(i),a=l.pending,a===null?(i.next=l.pending=i,wr(l,i)):(i.next=a.next,l.pending=a.next=i)}}function wr(e,l){var a=l.action,t=l.payload,n=e.state;if(l.isTransition){var i=N.T,u={};N.T=u;try{var s=a(n,t),f=N.S;f!==null&&f(u,s),Vr(e,l,s)}catch(v){Pc(e,l,v)}finally{i!==null&&u.types!==null&&(i.types=u.types),N.T=i}}else try{i=a(n,t),Vr(e,l,i)}catch(v){Pc(e,l,v)}}function Vr(e,l,a){a!==null&&typeof a=="object"&&typeof a.then=="function"?a.then(function(t){kr(e,l,t)},function(t){return Pc(e,l,t)}):kr(e,l,a)}function kr(e,l,a){l.status="fulfilled",l.value=a,Kr(l),e.state=a,l=e.pending,l!==null&&(a=l.next,a===l?e.pending=null:(a=a.next,l.next=a,wr(e,a)))}function Pc(e,l,a){var t=e.pending;if(e.pending=null,t!==null){t=t.next;do l.status="rejected",l.reason=a,Kr(l),l=l.next;while(l!==t)}e.action=null}function Kr(e){e=e.listeners;for(var l=0;l<e.length;l++)(0,e[l])()}function Jr(e,l){return l}function $r(e,l){if(te){var a=pe.formState;if(a!==null){e:{var t=$;if(te){if(ge){l:{for(var n=ge,i=Sl;n.nodeType!==8;){if(!i){n=null;break l}if(n=_l(n.nextSibling),n===null){n=null;break l}}i=n.data,n=i==="F!"||i==="F"?n:null}if(n){ge=_l(n.nextSibling),t=n.data==="F!";break e}}ta(t)}t=!1}t&&(l=a[0])}}return a=Je(),a.memoizedState=a.baseState=l,t={pending:null,lanes:0,dispatch:null,lastRenderedReducer:Jr,lastRenderedState:l},a.queue=t,a=pf.bind(null,$,t),t.dispatch=a,t=Fc(!1),i=nu.bind(null,$,!1,t.queue),t=Je(),n={state:l,dispatch:null,action:e,pending:null},t.queue=n,a=wm.bind(null,$,n,i,a),n.dispatch=a,t.memoizedState=e,[l,a,!1]}function Wr(e){var l=Ee();return Fr(l,de,e)}function Fr(e,l,a){if(l=$c(e,l,Jr)[0],e=ti(Ll)[0],typeof l=="object"&&l!==null&&typeof l.then=="function")try{var t=Ft(l)}catch(u){throw u===st?Kn:u}else t=l;l=Ee();var n=l.queue,i=n.dispatch;return a!==l.memoizedState&&($.flags|=2048,mt(9,{destroy:void 0},Vm.bind(null,n,a),null)),[t,i,e]}function Vm(e,l){e.action=l}function Pr(e){var l=Ee(),a=de;if(a!==null)return Fr(l,a,e);Ee(),l=l.memoizedState,a=Ee();var t=a.queue.dispatch;return a.memoizedState=e,[l,t,!1]}function mt(e,l,a,t){return e={tag:e,create:a,deps:t,inst:l,next:null},l=$.updateQueue,l===null&&(l=li(),$.updateQueue=l),a=l.lastEffect,a===null?l.lastEffect=e.next=e:(t=a.next,a.next=e,e.next=t,l.lastEffect=e),e}function Ir(){return Ee().memoizedState}function ni(e,l,a,t){var n=Je();$.flags|=e,n.memoizedState=mt(1|l,{destroy:void 0},a,t===void 0?null:t)}function ii(e,l,a,t){var n=Ee();t=t===void 0?null:t;var i=n.memoizedState.inst;de!==null&&t!==null&&Zc(t,de.memoizedState.deps)?n.memoizedState=mt(l,i,a,t):($.flags|=e,n.memoizedState=mt(1|l,i,a,t))}function ef(e,l){ni(8390656,8,e,l)}function Ic(e,l){ii(2048,8,e,l)}function km(e){$.flags|=4;var l=$.updateQueue;if(l===null)l=li(),$.updateQueue=l,l.events=[e];else{var a=l.events;a===null?l.events=[e]:a.push(e)}}function lf(e){var l=Ee().memoizedState;return km({ref:l,nextImpl:e}),function(){if((ce&2)!==0)throw Error(r(440));return l.impl.apply(void 0,arguments)}}function af(e,l){return ii(4,2,e,l)}function tf(e,l){return ii(4,4,e,l)}function nf(e,l){if(typeof l=="function"){e=e();var a=l(e);return function(){typeof a=="function"?a():l(null)}}if(l!=null)return e=e(),l.current=e,function(){l.current=null}}function cf(e,l,a){a=a!=null?a.concat([e]):null,ii(4,4,nf.bind(null,l,e),a)}function eu(){}function uf(e,l){var a=Ee();l=l===void 0?null:l;var t=a.memoizedState;return l!==null&&Zc(l,t[1])?t[0]:(a.memoizedState=[e,l],e)}function sf(e,l){var a=Ee();l=l===void 0?null:l;var t=a.memoizedState;if(l!==null&&Zc(l,t[1]))return t[0];if(t=e(),Ya){Pl(!0);try{e()}finally{Pl(!1)}}return a.memoizedState=[t,l],t}function lu(e,l,a){return a===void 0||(Ql&1073741824)!==0&&(le&261930)===0?e.memoizedState=l:(e.memoizedState=a,e=ro(),$.lanes|=e,da|=e,a)}function rf(e,l,a,t){return rl(a,l)?a:ft.current!==null?(e=lu(e,a,t),rl(e,l)||(De=!0),e):(Ql&42)===0||(Ql&1073741824)!==0&&(le&261930)===0?(De=!0,e.memoizedState=a):(e=ro(),$.lanes|=e,da|=e,l)}function ff(e,l,a,t,n){var i=R.p;R.p=i!==0&&8>i?i:8;var u=N.T,s={};N.T=s,nu(e,!1,l,a);try{var f=n(),v=N.S;if(v!==null&&v(s,f),f!==null&&typeof f=="object"&&typeof f.then=="function"){var S=Qm(f,t);Pt(e,l,S,pl(e))}else Pt(e,l,t,pl(e))}catch(z){Pt(e,l,{then:function(){},status:"rejected",reason:z},pl())}finally{R.p=i,u!==null&&s.types!==null&&(u.types=s.types),N.T=u}}function Km(){}function au(e,l,a,t){if(e.tag!==5)throw Error(r(476));var n=of(e).queue;ff(e,n,l,k,a===null?Km:function(){return df(e),a(t)})}function of(e){var l=e.memoizedState;if(l!==null)return l;l={memoizedState:k,baseState:k,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:Ll,lastRenderedState:k},next:null};var a={};return l.next={memoizedState:a,baseState:a,baseQueue:null,queue:{pending:null,lanes:0,dispatch:null,lastRenderedReducer:Ll,lastRenderedState:a},next:null},e.memoizedState=l,e=e.alternate,e!==null&&(e.memoizedState=l),l}function df(e){var l=of(e);l.next===null&&(l=e.alternate.memoizedState),Pt(e,l.next.queue,{},pl())}function tu(){return Qe(vn)}function mf(){return Ee().memoizedState}function hf(){return Ee().memoizedState}function Jm(e){for(var l=e.return;l!==null;){switch(l.tag){case 24:case 3:var a=pl();e=ca(a);var t=ua(l,e,a);t!==null&&(al(t,l,a),Kt(t,l,a)),l={cache:Uc()},e.payload=l;return}l=l.return}}function $m(e,l,a){var t=pl();a={lane:t,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null},ci(e)?vf(l,a):(a=jc(e,l,a,t),a!==null&&(al(a,e,t),gf(a,l,t)))}function pf(e,l,a){var t=pl();Pt(e,l,a,t)}function Pt(e,l,a,t){var n={lane:t,revertLane:0,gesture:null,action:a,hasEagerState:!1,eagerState:null,next:null};if(ci(e))vf(l,n);else{var i=e.alternate;if(e.lanes===0&&(i===null||i.lanes===0)&&(i=l.lastRenderedReducer,i!==null))try{var u=l.lastRenderedState,s=i(u,a);if(n.hasEagerState=!0,n.eagerState=s,rl(s,u))return Xn(e,l,n,0),pe===null&&Gn(),!1}catch{}if(a=jc(e,l,n,t),a!==null)return al(a,e,t),gf(a,l,t),!0}return!1}function nu(e,l,a,t){if(t={lane:2,revertLane:Bu(),gesture:null,action:t,hasEagerState:!1,eagerState:null,next:null},ci(e)){if(l)throw Error(r(479))}else l=jc(e,a,t,2),l!==null&&al(l,e,2)}function ci(e){var l=e.alternate;return e===$||l!==null&&l===$}function vf(e,l){ot=In=!0;var a=e.pending;a===null?l.next=l:(l.next=a.next,a.next=l),e.pending=l}function gf(e,l,a){if((a&4194048)!==0){var t=l.lanes;t&=e.pendingLanes,a|=t,l.lanes=a,js(e,a)}}var It={readContext:Qe,use:ai,useCallback:Se,useContext:Se,useEffect:Se,useImperativeHandle:Se,useLayoutEffect:Se,useInsertionEffect:Se,useMemo:Se,useReducer:Se,useRef:Se,useState:Se,useDebugValue:Se,useDeferredValue:Se,useTransition:Se,useSyncExternalStore:Se,useId:Se,useHostTransitionStatus:Se,useFormState:Se,useActionState:Se,useOptimistic:Se,useMemoCache:Se,useCacheRefresh:Se};It.useEffectEvent=Se;var yf={readContext:Qe,use:ai,useCallback:function(e,l){return Je().memoizedState=[e,l===void 0?null:l],e},useContext:Qe,useEffect:ef,useImperativeHandle:function(e,l,a){a=a!=null?a.concat([e]):null,ni(4194308,4,nf.bind(null,l,e),a)},useLayoutEffect:function(e,l){return ni(4194308,4,e,l)},useInsertionEffect:function(e,l){ni(4,2,e,l)},useMemo:function(e,l){var a=Je();l=l===void 0?null:l;var t=e();if(Ya){Pl(!0);try{e()}finally{Pl(!1)}}return a.memoizedState=[t,l],t},useReducer:function(e,l,a){var t=Je();if(a!==void 0){var n=a(l);if(Ya){Pl(!0);try{a(l)}finally{Pl(!1)}}}else n=l;return t.memoizedState=t.baseState=n,e={pending:null,lanes:0,dispatch:null,lastRenderedReducer:e,lastRenderedState:n},t.queue=e,e=e.dispatch=$m.bind(null,$,e),[t.memoizedState,e]},useRef:function(e){var l=Je();return e={current:e},l.memoizedState=e},useState:function(e){e=Fc(e);var l=e.queue,a=pf.bind(null,$,l);return l.dispatch=a,[e.memoizedState,a]},useDebugValue:eu,useDeferredValue:function(e,l){var a=Je();return lu(a,e,l)},useTransition:function(){var e=Fc(!1);return e=ff.bind(null,$,e.queue,!0,!1),Je().memoizedState=e,[!1,e]},useSyncExternalStore:function(e,l,a){var t=$,n=Je();if(te){if(a===void 0)throw Error(r(407));a=a()}else{if(a=l(),pe===null)throw Error(r(349));(le&127)!==0||Yr(t,l,a)}n.memoizedState=a;var i={value:a,getSnapshot:l};return n.queue=i,ef(Xr.bind(null,t,i,e),[e]),t.flags|=2048,mt(9,{destroy:void 0},Gr.bind(null,t,i,a,l),null),a},useId:function(){var e=Je(),l=pe.identifierPrefix;if(te){var a=Ml,t=Dl;a=(t&~(1<<32-sl(t)-1)).toString(32)+a,l="_"+l+"R_"+a,a=ei++,0<a&&(l+="H"+a.toString(32)),l+="_"}else a=Lm++,l="_"+l+"r_"+a.toString(32)+"_";return e.memoizedState=l},useHostTransitionStatus:tu,useFormState:$r,useActionState:$r,useOptimistic:function(e){var l=Je();l.memoizedState=l.baseState=e;var a={pending:null,lanes:0,dispatch:null,lastRenderedReducer:null,lastRenderedState:null};return l.queue=a,l=nu.bind(null,$,!0,a),a.dispatch=l,[e,l]},useMemoCache:Jc,useCacheRefresh:function(){return Je().memoizedState=Jm.bind(null,$)},useEffectEvent:function(e){var l=Je(),a={impl:e};return l.memoizedState=a,function(){if((ce&2)!==0)throw Error(r(440));return a.impl.apply(void 0,arguments)}}},iu={readContext:Qe,use:ai,useCallback:uf,useContext:Qe,useEffect:Ic,useImperativeHandle:cf,useInsertionEffect:af,useLayoutEffect:tf,useMemo:sf,useReducer:ti,useRef:Ir,useState:function(){return ti(Ll)},useDebugValue:eu,useDeferredValue:function(e,l){var a=Ee();return rf(a,de.memoizedState,e,l)},useTransition:function(){var e=ti(Ll)[0],l=Ee().memoizedState;return[typeof e=="boolean"?e:Ft(e),l]},useSyncExternalStore:qr,useId:mf,useHostTransitionStatus:tu,useFormState:Wr,useActionState:Wr,useOptimistic:function(e,l){var a=Ee();return Zr(a,de,e,l)},useMemoCache:Jc,useCacheRefresh:hf};iu.useEffectEvent=lf;var bf={readContext:Qe,use:ai,useCallback:uf,useContext:Qe,useEffect:Ic,useImperativeHandle:cf,useInsertionEffect:af,useLayoutEffect:tf,useMemo:sf,useReducer:Wc,useRef:Ir,useState:function(){return Wc(Ll)},useDebugValue:eu,useDeferredValue:function(e,l){var a=Ee();return de===null?lu(a,e,l):rf(a,de.memoizedState,e,l)},useTransition:function(){var e=Wc(Ll)[0],l=Ee().memoizedState;return[typeof e=="boolean"?e:Ft(e),l]},useSyncExternalStore:qr,useId:mf,useHostTransitionStatus:tu,useFormState:Pr,useActionState:Pr,useOptimistic:function(e,l){var a=Ee();return de!==null?Zr(a,de,e,l):(a.baseState=e,[e,a.queue.dispatch])},useMemoCache:Jc,useCacheRefresh:hf};bf.useEffectEvent=lf;function cu(e,l,a,t){l=e.memoizedState,a=a(t,l),a=a==null?l:A({},l,a),e.memoizedState=a,e.lanes===0&&(e.updateQueue.baseState=a)}var uu={enqueueSetState:function(e,l,a){e=e._reactInternals;var t=pl(),n=ca(t);n.payload=l,a!=null&&(n.callback=a),l=ua(e,n,t),l!==null&&(al(l,e,t),Kt(l,e,t))},enqueueReplaceState:function(e,l,a){e=e._reactInternals;var t=pl(),n=ca(t);n.tag=1,n.payload=l,a!=null&&(n.callback=a),l=ua(e,n,t),l!==null&&(al(l,e,t),Kt(l,e,t))},enqueueForceUpdate:function(e,l){e=e._reactInternals;var a=pl(),t=ca(a);t.tag=2,l!=null&&(t.callback=l),l=ua(e,t,a),l!==null&&(al(l,e,a),Kt(l,e,a))}};function xf(e,l,a,t,n,i,u){return e=e.stateNode,typeof e.shouldComponentUpdate=="function"?e.shouldComponentUpdate(t,i,u):l.prototype&&l.prototype.isPureReactComponent?!Gt(a,t)||!Gt(n,i):!0}function jf(e,l,a,t){e=l.state,typeof l.componentWillReceiveProps=="function"&&l.componentWillReceiveProps(a,t),typeof l.UNSAFE_componentWillReceiveProps=="function"&&l.UNSAFE_componentWillReceiveProps(a,t),l.state!==e&&uu.enqueueReplaceState(l,l.state,null)}function Ga(e,l){var a=l;if("ref"in l){a={};for(var t in l)t!=="ref"&&(a[t]=l[t])}if(e=e.defaultProps){a===l&&(a=A({},a));for(var n in e)a[n]===void 0&&(a[n]=e[n])}return a}function Sf(e){Yn(e)}function Nf(e){console.error(e)}function _f(e){Yn(e)}function ui(e,l){try{var a=e.onUncaughtError;a(l.value,{componentStack:l.stack})}catch(t){setTimeout(function(){throw t})}}function zf(e,l,a){try{var t=e.onCaughtError;t(a.value,{componentStack:a.stack,errorBoundary:l.tag===1?l.stateNode:null})}catch(n){setTimeout(function(){throw n})}}function su(e,l,a){return a=ca(a),a.tag=3,a.payload={element:null},a.callback=function(){ui(e,l)},a}function Tf(e){return e=ca(e),e.tag=3,e}function Ef(e,l,a,t){var n=a.type.getDerivedStateFromError;if(typeof n=="function"){var i=t.value;e.payload=function(){return n(i)},e.callback=function(){zf(l,a,t)}}var u=a.stateNode;u!==null&&typeof u.componentDidCatch=="function"&&(e.callback=function(){zf(l,a,t),typeof n!="function"&&(ma===null?ma=new Set([this]):ma.add(this));var s=t.stack;this.componentDidCatch(t.value,{componentStack:s!==null?s:""})})}function Wm(e,l,a,t,n){if(a.flags|=32768,t!==null&&typeof t=="object"&&typeof t.then=="function"){if(l=a.alternate,l!==null&&it(l,a,n,!0),a=ol.current,a!==null){switch(a.tag){case 31:case 13:return Nl===null?bi():a.alternate===null&&Ne===0&&(Ne=3),a.flags&=-257,a.flags|=65536,a.lanes=n,t===Jn?a.flags|=16384:(l=a.updateQueue,l===null?a.updateQueue=new Set([t]):l.add(t),Cu(e,t,n)),!1;case 22:return a.flags|=65536,t===Jn?a.flags|=16384:(l=a.updateQueue,l===null?(l={transitions:null,markerInstances:null,retryQueue:new Set([t])},a.updateQueue=l):(a=l.retryQueue,a===null?l.retryQueue=new Set([t]):a.add(t)),Cu(e,t,n)),!1}throw Error(r(435,a.tag))}return Cu(e,t,n),bi(),!1}if(te)return l=ol.current,l!==null?((l.flags&65536)===0&&(l.flags|=256),l.flags|=65536,l.lanes=n,t!==Ec&&(e=Error(r(422),{cause:t}),Lt(bl(e,a)))):(t!==Ec&&(l=Error(r(423),{cause:t}),Lt(bl(l,a))),e=e.current.alternate,e.flags|=65536,n&=-n,e.lanes|=n,t=bl(t,a),n=su(e.stateNode,t,n),Yc(e,n),Ne!==4&&(Ne=2)),!1;var i=Error(r(520),{cause:t});if(i=bl(i,a),sn===null?sn=[i]:sn.push(i),Ne!==4&&(Ne=2),l===null)return!0;t=bl(t,a),a=l;do{switch(a.tag){case 3:return a.flags|=65536,e=n&-n,a.lanes|=e,e=su(a.stateNode,t,e),Yc(a,e),!1;case 1:if(l=a.type,i=a.stateNode,(a.flags&128)===0&&(typeof l.getDerivedStateFromError=="function"||i!==null&&typeof i.componentDidCatch=="function"&&(ma===null||!ma.has(i))))return a.flags|=65536,n&=-n,a.lanes|=n,n=Tf(n),Ef(n,e,a,t),Yc(a,n),!1}a=a.return}while(a!==null);return!1}var ru=Error(r(461)),De=!1;function Le(e,l,a,t){l.child=e===null?Dr(l,null,a,t):qa(l,e.child,a,t)}function Af(e,l,a,t,n){a=a.render;var i=l.ref;if("ref"in t){var u={};for(var s in t)s!=="ref"&&(u[s]=t[s])}else u=t;return Ca(l),t=wc(e,l,a,u,i,n),s=Vc(),e!==null&&!De?(kc(e,l,n),Zl(e,l,n)):(te&&s&&zc(l),l.flags|=1,Le(e,l,t,n),l.child)}function Of(e,l,a,t,n){if(e===null){var i=a.type;return typeof i=="function"&&!Sc(i)&&i.defaultProps===void 0&&a.compare===null?(l.tag=15,l.type=i,Df(e,l,i,t,n)):(e=Ln(a.type,null,t,l,l.mode,n),e.ref=l.ref,e.return=l,l.child=e)}if(i=e.child,!gu(e,n)){var u=i.memoizedProps;if(a=a.compare,a=a!==null?a:Gt,a(u,t)&&e.ref===l.ref)return Zl(e,l,n)}return l.flags|=1,e=ql(i,t),e.ref=l.ref,e.return=l,l.child=e}function Df(e,l,a,t,n){if(e!==null){var i=e.memoizedProps;if(Gt(i,t)&&e.ref===l.ref)if(De=!1,l.pendingProps=t=i,gu(e,n))(e.flags&131072)!==0&&(De=!0);else return l.lanes=e.lanes,Zl(e,l,n)}return fu(e,l,a,t,n)}function Mf(e,l,a,t){var n=t.children,i=e!==null?e.memoizedState:null;if(e===null&&l.stateNode===null&&(l.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),t.mode==="hidden"){if((l.flags&128)!==0){if(i=i!==null?i.baseLanes|a:a,e!==null){for(t=l.child=e.child,n=0;t!==null;)n=n|t.lanes|t.childLanes,t=t.sibling;t=n&~i}else t=0,l.child=null;return Uf(e,l,i,a,t)}if((a&536870912)!==0)l.memoizedState={baseLanes:0,cachePool:null},e!==null&&kn(l,i!==null?i.cachePool:null),i!==null?Cr(l,i):Xc(),Rr(l);else return t=l.lanes=536870912,Uf(e,l,i!==null?i.baseLanes|a:a,a,t)}else i!==null?(kn(l,i.cachePool),Cr(l,i),ra(),l.memoizedState=null):(e!==null&&kn(l,null),Xc(),ra());return Le(e,l,n,a),l.child}function en(e,l){return e!==null&&e.tag===22||l.stateNode!==null||(l.stateNode={_visibility:1,_pendingMarkers:null,_retryCache:null,_transitions:null}),l.sibling}function Uf(e,l,a,t,n){var i=Rc();return i=i===null?null:{parent:Ae._currentValue,pool:i},l.memoizedState={baseLanes:a,cachePool:i},e!==null&&kn(l,null),Xc(),Rr(l),e!==null&&it(e,l,t,!0),l.childLanes=n,null}function si(e,l){return l=fi({mode:l.mode,children:l.children},e.mode),l.ref=e.ref,e.child=l,l.return=e,l}function Cf(e,l,a){return qa(l,e.child,null,a),e=si(l,l.pendingProps),e.flags|=2,dl(l),l.memoizedState=null,e}function Fm(e,l,a){var t=l.pendingProps,n=(l.flags&128)!==0;if(l.flags&=-129,e===null){if(te){if(t.mode==="hidden")return e=si(l,t),l.lanes=536870912,en(null,e);if(Lc(l),(e=ge)?(e=ko(e,Sl),e=e!==null&&e.data==="&"?e:null,e!==null&&(l.memoizedState={dehydrated:e,treeContext:la!==null?{id:Dl,overflow:Ml}:null,retryLane:536870912,hydrationErrors:null},a=pr(e),a.return=l,l.child=a,Xe=l,ge=null)):e=null,e===null)throw ta(l);return l.lanes=536870912,null}return si(l,t)}var i=e.memoizedState;if(i!==null){var u=i.dehydrated;if(Lc(l),n)if(l.flags&256)l.flags&=-257,l=Cf(e,l,a);else if(l.memoizedState!==null)l.child=e.child,l.flags|=128,l=null;else throw Error(r(558));else if(De||it(e,l,a,!1),n=(a&e.childLanes)!==0,De||n){if(t=pe,t!==null&&(u=Ss(t,a),u!==0&&u!==i.retryLane))throw i.retryLane=u,Oa(e,u),al(t,e,u),ru;bi(),l=Cf(e,l,a)}else e=i.treeContext,ge=_l(u.nextSibling),Xe=l,te=!0,aa=null,Sl=!1,e!==null&&yr(l,e),l=si(l,t),l.flags|=4096;return l}return e=ql(e.child,{mode:t.mode,children:t.children}),e.ref=l.ref,l.child=e,e.return=l,e}function ri(e,l){var a=l.ref;if(a===null)e!==null&&e.ref!==null&&(l.flags|=4194816);else{if(typeof a!="function"&&typeof a!="object")throw Error(r(284));(e===null||e.ref!==a)&&(l.flags|=4194816)}}function fu(e,l,a,t,n){return Ca(l),a=wc(e,l,a,t,void 0,n),t=Vc(),e!==null&&!De?(kc(e,l,n),Zl(e,l,n)):(te&&t&&zc(l),l.flags|=1,Le(e,l,a,n),l.child)}function Rf(e,l,a,t,n,i){return Ca(l),l.updateQueue=null,a=Br(l,t,a,n),Hr(e),t=Vc(),e!==null&&!De?(kc(e,l,i),Zl(e,l,i)):(te&&t&&zc(l),l.flags|=1,Le(e,l,a,i),l.child)}function Hf(e,l,a,t,n){if(Ca(l),l.stateNode===null){var i=lt,u=a.contextType;typeof u=="object"&&u!==null&&(i=Qe(u)),i=new a(t,i),l.memoizedState=i.state!==null&&i.state!==void 0?i.state:null,i.updater=uu,l.stateNode=i,i._reactInternals=l,i=l.stateNode,i.props=t,i.state=l.memoizedState,i.refs={},Bc(l),u=a.contextType,i.context=typeof u=="object"&&u!==null?Qe(u):lt,i.state=l.memoizedState,u=a.getDerivedStateFromProps,typeof u=="function"&&(cu(l,a,u,t),i.state=l.memoizedState),typeof a.getDerivedStateFromProps=="function"||typeof i.getSnapshotBeforeUpdate=="function"||typeof i.UNSAFE_componentWillMount!="function"&&typeof i.componentWillMount!="function"||(u=i.state,typeof i.componentWillMount=="function"&&i.componentWillMount(),typeof i.UNSAFE_componentWillMount=="function"&&i.UNSAFE_componentWillMount(),u!==i.state&&uu.enqueueReplaceState(i,i.state,null),$t(l,t,i,n),Jt(),i.state=l.memoizedState),typeof i.componentDidMount=="function"&&(l.flags|=4194308),t=!0}else if(e===null){i=l.stateNode;var s=l.memoizedProps,f=Ga(a,s);i.props=f;var v=i.context,S=a.contextType;u=lt,typeof S=="object"&&S!==null&&(u=Qe(S));var z=a.getDerivedStateFromProps;S=typeof z=="function"||typeof i.getSnapshotBeforeUpdate=="function",s=l.pendingProps!==s,S||typeof i.UNSAFE_componentWillReceiveProps!="function"&&typeof i.componentWillReceiveProps!="function"||(s||v!==u)&&jf(l,i,t,u),ia=!1;var g=l.memoizedState;i.state=g,$t(l,t,i,n),Jt(),v=l.memoizedState,s||g!==v||ia?(typeof z=="function"&&(cu(l,a,z,t),v=l.memoizedState),(f=ia||xf(l,a,f,t,g,v,u))?(S||typeof i.UNSAFE_componentWillMount!="function"&&typeof i.componentWillMount!="function"||(typeof i.componentWillMount=="function"&&i.componentWillMount(),typeof i.UNSAFE_componentWillMount=="function"&&i.UNSAFE_componentWillMount()),typeof i.componentDidMount=="function"&&(l.flags|=4194308)):(typeof i.componentDidMount=="function"&&(l.flags|=4194308),l.memoizedProps=t,l.memoizedState=v),i.props=t,i.state=v,i.context=u,t=f):(typeof i.componentDidMount=="function"&&(l.flags|=4194308),t=!1)}else{i=l.stateNode,qc(e,l),u=l.memoizedProps,S=Ga(a,u),i.props=S,z=l.pendingProps,g=i.context,v=a.contextType,f=lt,typeof v=="object"&&v!==null&&(f=Qe(v)),s=a.getDerivedStateFromProps,(v=typeof s=="function"||typeof i.getSnapshotBeforeUpdate=="function")||typeof i.UNSAFE_componentWillReceiveProps!="function"&&typeof i.componentWillReceiveProps!="function"||(u!==z||g!==f)&&jf(l,i,t,f),ia=!1,g=l.memoizedState,i.state=g,$t(l,t,i,n),Jt();var x=l.memoizedState;u!==z||g!==x||ia||e!==null&&e.dependencies!==null&&wn(e.dependencies)?(typeof s=="function"&&(cu(l,a,s,t),x=l.memoizedState),(S=ia||xf(l,a,S,t,g,x,f)||e!==null&&e.dependencies!==null&&wn(e.dependencies))?(v||typeof i.UNSAFE_componentWillUpdate!="function"&&typeof i.componentWillUpdate!="function"||(typeof i.componentWillUpdate=="function"&&i.componentWillUpdate(t,x,f),typeof i.UNSAFE_componentWillUpdate=="function"&&i.UNSAFE_componentWillUpdate(t,x,f)),typeof i.componentDidUpdate=="function"&&(l.flags|=4),typeof i.getSnapshotBeforeUpdate=="function"&&(l.flags|=1024)):(typeof i.componentDidUpdate!="function"||u===e.memoizedProps&&g===e.memoizedState||(l.flags|=4),typeof i.getSnapshotBeforeUpdate!="function"||u===e.memoizedProps&&g===e.memoizedState||(l.flags|=1024),l.memoizedProps=t,l.memoizedState=x),i.props=t,i.state=x,i.context=f,t=S):(typeof i.componentDidUpdate!="function"||u===e.memoizedProps&&g===e.memoizedState||(l.flags|=4),typeof i.getSnapshotBeforeUpdate!="function"||u===e.memoizedProps&&g===e.memoizedState||(l.flags|=1024),t=!1)}return i=t,ri(e,l),t=(l.flags&128)!==0,i||t?(i=l.stateNode,a=t&&typeof a.getDerivedStateFromError!="function"?null:i.render(),l.flags|=1,e!==null&&t?(l.child=qa(l,e.child,null,n),l.child=qa(l,null,a,n)):Le(e,l,a,n),l.memoizedState=i.state,e=l.child):e=Zl(e,l,n),e}function Bf(e,l,a,t){return Ma(),l.flags|=256,Le(e,l,a,t),l.child}var ou={dehydrated:null,treeContext:null,retryLane:0,hydrationErrors:null};function du(e){return{baseLanes:e,cachePool:_r()}}function mu(e,l,a){return e=e!==null?e.childLanes&~a:0,l&&(e|=hl),e}function qf(e,l,a){var t=l.pendingProps,n=!1,i=(l.flags&128)!==0,u;if((u=i)||(u=e!==null&&e.memoizedState===null?!1:(Te.current&2)!==0),u&&(n=!0,l.flags&=-129),u=(l.flags&32)!==0,l.flags&=-33,e===null){if(te){if(n?sa(l):ra(),(e=ge)?(e=ko(e,Sl),e=e!==null&&e.data!=="&"?e:null,e!==null&&(l.memoizedState={dehydrated:e,treeContext:la!==null?{id:Dl,overflow:Ml}:null,retryLane:536870912,hydrationErrors:null},a=pr(e),a.return=l,l.child=a,Xe=l,ge=null)):e=null,e===null)throw ta(l);return $u(e)?l.lanes=32:l.lanes=536870912,null}var s=t.children;return t=t.fallback,n?(ra(),n=l.mode,s=fi({mode:"hidden",children:s},n),t=Da(t,n,a,null),s.return=l,t.return=l,s.sibling=t,l.child=s,t=l.child,t.memoizedState=du(a),t.childLanes=mu(e,u,a),l.memoizedState=ou,en(null,t)):(sa(l),hu(l,s))}var f=e.memoizedState;if(f!==null&&(s=f.dehydrated,s!==null)){if(i)l.flags&256?(sa(l),l.flags&=-257,l=pu(e,l,a)):l.memoizedState!==null?(ra(),l.child=e.child,l.flags|=128,l=null):(ra(),s=t.fallback,n=l.mode,t=fi({mode:"visible",children:t.children},n),s=Da(s,n,a,null),s.flags|=2,t.return=l,s.return=l,t.sibling=s,l.child=t,qa(l,e.child,null,a),t=l.child,t.memoizedState=du(a),t.childLanes=mu(e,u,a),l.memoizedState=ou,l=en(null,t));else if(sa(l),$u(s)){if(u=s.nextSibling&&s.nextSibling.dataset,u)var v=u.dgst;u=v,t=Error(r(419)),t.stack="",t.digest=u,Lt({value:t,source:null,stack:null}),l=pu(e,l,a)}else if(De||it(e,l,a,!1),u=(a&e.childLanes)!==0,De||u){if(u=pe,u!==null&&(t=Ss(u,a),t!==0&&t!==f.retryLane))throw f.retryLane=t,Oa(e,t),al(u,e,t),ru;Ju(s)||bi(),l=pu(e,l,a)}else Ju(s)?(l.flags|=192,l.child=e.child,l=null):(e=f.treeContext,ge=_l(s.nextSibling),Xe=l,te=!0,aa=null,Sl=!1,e!==null&&yr(l,e),l=hu(l,t.children),l.flags|=4096);return l}return n?(ra(),s=t.fallback,n=l.mode,f=e.child,v=f.sibling,t=ql(f,{mode:"hidden",children:t.children}),t.subtreeFlags=f.subtreeFlags&65011712,v!==null?s=ql(v,s):(s=Da(s,n,a,null),s.flags|=2),s.return=l,t.return=l,t.sibling=s,l.child=t,en(null,t),t=l.child,s=e.child.memoizedState,s===null?s=du(a):(n=s.cachePool,n!==null?(f=Ae._currentValue,n=n.parent!==f?{parent:f,pool:f}:n):n=_r(),s={baseLanes:s.baseLanes|a,cachePool:n}),t.memoizedState=s,t.childLanes=mu(e,u,a),l.memoizedState=ou,en(e.child,t)):(sa(l),a=e.child,e=a.sibling,a=ql(a,{mode:"visible",children:t.children}),a.return=l,a.sibling=null,e!==null&&(u=l.deletions,u===null?(l.deletions=[e],l.flags|=16):u.push(e)),l.child=a,l.memoizedState=null,a)}function hu(e,l){return l=fi({mode:"visible",children:l},e.mode),l.return=e,e.child=l}function fi(e,l){return e=fl(22,e,null,l),e.lanes=0,e}function pu(e,l,a){return qa(l,e.child,null,a),e=hu(l,l.pendingProps.children),e.flags|=2,l.memoizedState=null,e}function Yf(e,l,a){e.lanes|=l;var t=e.alternate;t!==null&&(t.lanes|=l),Dc(e.return,l,a)}function vu(e,l,a,t,n,i){var u=e.memoizedState;u===null?e.memoizedState={isBackwards:l,rendering:null,renderingStartTime:0,last:t,tail:a,tailMode:n,treeForkCount:i}:(u.isBackwards=l,u.rendering=null,u.renderingStartTime=0,u.last=t,u.tail=a,u.tailMode=n,u.treeForkCount=i)}function Gf(e,l,a){var t=l.pendingProps,n=t.revealOrder,i=t.tail;t=t.children;var u=Te.current,s=(u&2)!==0;if(s?(u=u&1|2,l.flags|=128):u&=1,C(Te,u),Le(e,l,t,a),t=te?Qt:0,!s&&e!==null&&(e.flags&128)!==0)e:for(e=l.child;e!==null;){if(e.tag===13)e.memoizedState!==null&&Yf(e,a,l);else if(e.tag===19)Yf(e,a,l);else if(e.child!==null){e.child.return=e,e=e.child;continue}if(e===l)break e;for(;e.sibling===null;){if(e.return===null||e.return===l)break e;e=e.return}e.sibling.return=e.return,e=e.sibling}switch(n){case"forwards":for(a=l.child,n=null;a!==null;)e=a.alternate,e!==null&&Pn(e)===null&&(n=a),a=a.sibling;a=n,a===null?(n=l.child,l.child=null):(n=a.sibling,a.sibling=null),vu(l,!1,n,a,i,t);break;case"backwards":case"unstable_legacy-backwards":for(a=null,n=l.child,l.child=null;n!==null;){if(e=n.alternate,e!==null&&Pn(e)===null){l.child=n;break}e=n.sibling,n.sibling=a,a=n,n=e}vu(l,!0,a,null,i,t);break;case"together":vu(l,!1,null,null,void 0,t);break;default:l.memoizedState=null}return l.child}function Zl(e,l,a){if(e!==null&&(l.dependencies=e.dependencies),da|=l.lanes,(a&l.childLanes)===0)if(e!==null){if(it(e,l,a,!1),(a&l.childLanes)===0)return null}else return null;if(e!==null&&l.child!==e.child)throw Error(r(153));if(l.child!==null){for(e=l.child,a=ql(e,e.pendingProps),l.child=a,a.return=l;e.sibling!==null;)e=e.sibling,a=a.sibling=ql(e,e.pendingProps),a.return=l;a.sibling=null}return l.child}function gu(e,l){return(e.lanes&l)!==0?!0:(e=e.dependencies,!!(e!==null&&wn(e)))}function Pm(e,l,a){switch(l.tag){case 3:Ye(l,l.stateNode.containerInfo),na(l,Ae,e.memoizedState.cache),Ma();break;case 27:case 5:Tt(l);break;case 4:Ye(l,l.stateNode.containerInfo);break;case 10:na(l,l.type,l.memoizedProps.value);break;case 31:if(l.memoizedState!==null)return l.flags|=128,Lc(l),null;break;case 13:var t=l.memoizedState;if(t!==null)return t.dehydrated!==null?(sa(l),l.flags|=128,null):(a&l.child.childLanes)!==0?qf(e,l,a):(sa(l),e=Zl(e,l,a),e!==null?e.sibling:null);sa(l);break;case 19:var n=(e.flags&128)!==0;if(t=(a&l.childLanes)!==0,t||(it(e,l,a,!1),t=(a&l.childLanes)!==0),n){if(t)return Gf(e,l,a);l.flags|=128}if(n=l.memoizedState,n!==null&&(n.rendering=null,n.tail=null,n.lastEffect=null),C(Te,Te.current),t)break;return null;case 22:return l.lanes=0,Mf(e,l,a,l.pendingProps);case 24:na(l,Ae,e.memoizedState.cache)}return Zl(e,l,a)}function Xf(e,l,a){if(e!==null)if(e.memoizedProps!==l.pendingProps)De=!0;else{if(!gu(e,a)&&(l.flags&128)===0)return De=!1,Pm(e,l,a);De=(e.flags&131072)!==0}else De=!1,te&&(l.flags&1048576)!==0&&gr(l,Qt,l.index);switch(l.lanes=0,l.tag){case 16:e:{var t=l.pendingProps;if(e=Ha(l.elementType),l.type=e,typeof e=="function")Sc(e)?(t=Ga(e,t),l.tag=1,l=Hf(null,l,e,t,a)):(l.tag=0,l=fu(null,l,e,t,a));else{if(e!=null){var n=e.$$typeof;if(n===ke){l.tag=11,l=Af(null,l,e,t,a);break e}else if(n===P){l.tag=14,l=Of(null,l,e,t,a);break e}}throw l=we(e)||e,Error(r(306,l,""))}}return l;case 0:return fu(e,l,l.type,l.pendingProps,a);case 1:return t=l.type,n=Ga(t,l.pendingProps),Hf(e,l,t,n,a);case 3:e:{if(Ye(l,l.stateNode.containerInfo),e===null)throw Error(r(387));t=l.pendingProps;var i=l.memoizedState;n=i.element,qc(e,l),$t(l,t,null,a);var u=l.memoizedState;if(t=u.cache,na(l,Ae,t),t!==i.cache&&Mc(l,[Ae],a,!0),Jt(),t=u.element,i.isDehydrated)if(i={element:t,isDehydrated:!1,cache:u.cache},l.updateQueue.baseState=i,l.memoizedState=i,l.flags&256){l=Bf(e,l,t,a);break e}else if(t!==n){n=bl(Error(r(424)),l),Lt(n),l=Bf(e,l,t,a);break e}else for(e=l.stateNode.containerInfo,e.nodeType===9?e=e.body:e=e.nodeName==="HTML"?e.ownerDocument.body:e,ge=_l(e.firstChild),Xe=l,te=!0,aa=null,Sl=!0,a=Dr(l,null,t,a),l.child=a;a;)a.flags=a.flags&-3|4096,a=a.sibling;else{if(Ma(),t===n){l=Zl(e,l,a);break e}Le(e,l,t,a)}l=l.child}return l;case 26:return ri(e,l),e===null?(a=Po(l.type,null,l.pendingProps,null))?l.memoizedState=a:te||(a=l.type,e=l.pendingProps,t=Ti(X.current).createElement(a),t[Ge]=l,t[We]=e,Ze(t,a,e),He(t),l.stateNode=t):l.memoizedState=Po(l.type,e.memoizedProps,l.pendingProps,e.memoizedState),null;case 27:return Tt(l),e===null&&te&&(t=l.stateNode=$o(l.type,l.pendingProps,X.current),Xe=l,Sl=!0,n=ge,ga(l.type)?(Wu=n,ge=_l(t.firstChild)):ge=n),Le(e,l,l.pendingProps.children,a),ri(e,l),e===null&&(l.flags|=4194304),l.child;case 5:return e===null&&te&&((n=t=ge)&&(t=Ah(t,l.type,l.pendingProps,Sl),t!==null?(l.stateNode=t,Xe=l,ge=_l(t.firstChild),Sl=!1,n=!0):n=!1),n||ta(l)),Tt(l),n=l.type,i=l.pendingProps,u=e!==null?e.memoizedProps:null,t=i.children,Vu(n,i)?t=null:u!==null&&Vu(n,u)&&(l.flags|=32),l.memoizedState!==null&&(n=wc(e,l,Zm,null,null,a),vn._currentValue=n),ri(e,l),Le(e,l,t,a),l.child;case 6:return e===null&&te&&((e=a=ge)&&(a=Oh(a,l.pendingProps,Sl),a!==null?(l.stateNode=a,Xe=l,ge=null,e=!0):e=!1),e||ta(l)),null;case 13:return qf(e,l,a);case 4:return Ye(l,l.stateNode.containerInfo),t=l.pendingProps,e===null?l.child=qa(l,null,t,a):Le(e,l,t,a),l.child;case 11:return Af(e,l,l.type,l.pendingProps,a);case 7:return Le(e,l,l.pendingProps,a),l.child;case 8:return Le(e,l,l.pendingProps.children,a),l.child;case 12:return Le(e,l,l.pendingProps.children,a),l.child;case 10:return t=l.pendingProps,na(l,l.type,t.value),Le(e,l,t.children,a),l.child;case 9:return n=l.type._context,t=l.pendingProps.children,Ca(l),n=Qe(n),t=t(n),l.flags|=1,Le(e,l,t,a),l.child;case 14:return Of(e,l,l.type,l.pendingProps,a);case 15:return Df(e,l,l.type,l.pendingProps,a);case 19:return Gf(e,l,a);case 31:return Fm(e,l,a);case 22:return Mf(e,l,a,l.pendingProps);case 24:return Ca(l),t=Qe(Ae),e===null?(n=Rc(),n===null&&(n=pe,i=Uc(),n.pooledCache=i,i.refCount++,i!==null&&(n.pooledCacheLanes|=a),n=i),l.memoizedState={parent:t,cache:n},Bc(l),na(l,Ae,n)):((e.lanes&a)!==0&&(qc(e,l),$t(l,null,null,a),Jt()),n=e.memoizedState,i=l.memoizedState,n.parent!==t?(n={parent:t,cache:t},l.memoizedState=n,l.lanes===0&&(l.memoizedState=l.updateQueue.baseState=n),na(l,Ae,t)):(t=i.cache,na(l,Ae,t),t!==n.cache&&Mc(l,[Ae],a,!0))),Le(e,l,l.pendingProps.children,a),l.child;case 29:throw l.pendingProps}throw Error(r(156,l.tag))}function wl(e){e.flags|=4}function yu(e,l,a,t,n){if((l=(e.mode&32)!==0)&&(l=!1),l){if(e.flags|=16777216,(n&335544128)===n)if(e.stateNode.complete)e.flags|=8192;else if(ho())e.flags|=8192;else throw Ba=Jn,Hc}else e.flags&=-16777217}function Qf(e,l){if(l.type!=="stylesheet"||(l.state.loading&4)!==0)e.flags&=-16777217;else if(e.flags|=16777216,!td(l))if(ho())e.flags|=8192;else throw Ba=Jn,Hc}function oi(e,l){l!==null&&(e.flags|=4),e.flags&16384&&(l=e.tag!==22?bs():536870912,e.lanes|=l,gt|=l)}function ln(e,l){if(!te)switch(e.tailMode){case"hidden":l=e.tail;for(var a=null;l!==null;)l.alternate!==null&&(a=l),l=l.sibling;a===null?e.tail=null:a.sibling=null;break;case"collapsed":a=e.tail;for(var t=null;a!==null;)a.alternate!==null&&(t=a),a=a.sibling;t===null?l||e.tail===null?e.tail=null:e.tail.sibling=null:t.sibling=null}}function ye(e){var l=e.alternate!==null&&e.alternate.child===e.child,a=0,t=0;if(l)for(var n=e.child;n!==null;)a|=n.lanes|n.childLanes,t|=n.subtreeFlags&65011712,t|=n.flags&65011712,n.return=e,n=n.sibling;else for(n=e.child;n!==null;)a|=n.lanes|n.childLanes,t|=n.subtreeFlags,t|=n.flags,n.return=e,n=n.sibling;return e.subtreeFlags|=t,e.childLanes=a,l}function Im(e,l,a){var t=l.pendingProps;switch(Tc(l),l.tag){case 16:case 15:case 0:case 11:case 7:case 8:case 12:case 9:case 14:return ye(l),null;case 1:return ye(l),null;case 3:return a=l.stateNode,t=null,e!==null&&(t=e.memoizedState.cache),l.memoizedState.cache!==t&&(l.flags|=2048),Xl(Ae),ze(),a.pendingContext&&(a.context=a.pendingContext,a.pendingContext=null),(e===null||e.child===null)&&(nt(l)?wl(l):e===null||e.memoizedState.isDehydrated&&(l.flags&256)===0||(l.flags|=1024,Ac())),ye(l),null;case 26:var n=l.type,i=l.memoizedState;return e===null?(wl(l),i!==null?(ye(l),Qf(l,i)):(ye(l),yu(l,n,null,t,a))):i?i!==e.memoizedState?(wl(l),ye(l),Qf(l,i)):(ye(l),l.flags&=-16777217):(e=e.memoizedProps,e!==t&&wl(l),ye(l),yu(l,n,e,t,a)),null;case 27:if(Sn(l),a=X.current,n=l.type,e!==null&&l.stateNode!=null)e.memoizedProps!==t&&wl(l);else{if(!t){if(l.stateNode===null)throw Error(r(166));return ye(l),null}e=M.current,nt(l)?br(l):(e=$o(n,t,a),l.stateNode=e,wl(l))}return ye(l),null;case 5:if(Sn(l),n=l.type,e!==null&&l.stateNode!=null)e.memoizedProps!==t&&wl(l);else{if(!t){if(l.stateNode===null)throw Error(r(166));return ye(l),null}if(i=M.current,nt(l))br(l);else{var u=Ti(X.current);switch(i){case 1:i=u.createElementNS("http://www.w3.org/2000/svg",n);break;case 2:i=u.createElementNS("http://www.w3.org/1998/Math/MathML",n);break;default:switch(n){case"svg":i=u.createElementNS("http://www.w3.org/2000/svg",n);break;case"math":i=u.createElementNS("http://www.w3.org/1998/Math/MathML",n);break;case"script":i=u.createElement("div"),i.innerHTML="<script><\/script>",i=i.removeChild(i.firstChild);break;case"select":i=typeof t.is=="string"?u.createElement("select",{is:t.is}):u.createElement("select"),t.multiple?i.multiple=!0:t.size&&(i.size=t.size);break;default:i=typeof t.is=="string"?u.createElement(n,{is:t.is}):u.createElement(n)}}i[Ge]=l,i[We]=t;e:for(u=l.child;u!==null;){if(u.tag===5||u.tag===6)i.appendChild(u.stateNode);else if(u.tag!==4&&u.tag!==27&&u.child!==null){u.child.return=u,u=u.child;continue}if(u===l)break e;for(;u.sibling===null;){if(u.return===null||u.return===l)break e;u=u.return}u.sibling.return=u.return,u=u.sibling}l.stateNode=i;e:switch(Ze(i,n,t),n){case"button":case"input":case"select":case"textarea":t=!!t.autoFocus;break e;case"img":t=!0;break e;default:t=!1}t&&wl(l)}}return ye(l),yu(l,l.type,e===null?null:e.memoizedProps,l.pendingProps,a),null;case 6:if(e&&l.stateNode!=null)e.memoizedProps!==t&&wl(l);else{if(typeof t!="string"&&l.stateNode===null)throw Error(r(166));if(e=X.current,nt(l)){if(e=l.stateNode,a=l.memoizedProps,t=null,n=Xe,n!==null)switch(n.tag){case 27:case 5:t=n.memoizedProps}e[Ge]=l,e=!!(e.nodeValue===a||t!==null&&t.suppressHydrationWarning===!0||Yo(e.nodeValue,a)),e||ta(l,!0)}else e=Ti(e).createTextNode(t),e[Ge]=l,l.stateNode=e}return ye(l),null;case 31:if(a=l.memoizedState,e===null||e.memoizedState!==null){if(t=nt(l),a!==null){if(e===null){if(!t)throw Error(r(318));if(e=l.memoizedState,e=e!==null?e.dehydrated:null,!e)throw Error(r(557));e[Ge]=l}else Ma(),(l.flags&128)===0&&(l.memoizedState=null),l.flags|=4;ye(l),e=!1}else a=Ac(),e!==null&&e.memoizedState!==null&&(e.memoizedState.hydrationErrors=a),e=!0;if(!e)return l.flags&256?(dl(l),l):(dl(l),null);if((l.flags&128)!==0)throw Error(r(558))}return ye(l),null;case 13:if(t=l.memoizedState,e===null||e.memoizedState!==null&&e.memoizedState.dehydrated!==null){if(n=nt(l),t!==null&&t.dehydrated!==null){if(e===null){if(!n)throw Error(r(318));if(n=l.memoizedState,n=n!==null?n.dehydrated:null,!n)throw Error(r(317));n[Ge]=l}else Ma(),(l.flags&128)===0&&(l.memoizedState=null),l.flags|=4;ye(l),n=!1}else n=Ac(),e!==null&&e.memoizedState!==null&&(e.memoizedState.hydrationErrors=n),n=!0;if(!n)return l.flags&256?(dl(l),l):(dl(l),null)}return dl(l),(l.flags&128)!==0?(l.lanes=a,l):(a=t!==null,e=e!==null&&e.memoizedState!==null,a&&(t=l.child,n=null,t.alternate!==null&&t.alternate.memoizedState!==null&&t.alternate.memoizedState.cachePool!==null&&(n=t.alternate.memoizedState.cachePool.pool),i=null,t.memoizedState!==null&&t.memoizedState.cachePool!==null&&(i=t.memoizedState.cachePool.pool),i!==n&&(t.flags|=2048)),a!==e&&a&&(l.child.flags|=8192),oi(l,l.updateQueue),ye(l),null);case 4:return ze(),e===null&&Xu(l.stateNode.containerInfo),ye(l),null;case 10:return Xl(l.type),ye(l),null;case 19:if(T(Te),t=l.memoizedState,t===null)return ye(l),null;if(n=(l.flags&128)!==0,i=t.rendering,i===null)if(n)ln(t,!1);else{if(Ne!==0||e!==null&&(e.flags&128)!==0)for(e=l.child;e!==null;){if(i=Pn(e),i!==null){for(l.flags|=128,ln(t,!1),e=i.updateQueue,l.updateQueue=e,oi(l,e),l.subtreeFlags=0,e=a,a=l.child;a!==null;)hr(a,e),a=a.sibling;return C(Te,Te.current&1|2),te&&Yl(l,t.treeForkCount),l.child}e=e.sibling}t.tail!==null&&cl()>vi&&(l.flags|=128,n=!0,ln(t,!1),l.lanes=4194304)}else{if(!n)if(e=Pn(i),e!==null){if(l.flags|=128,n=!0,e=e.updateQueue,l.updateQueue=e,oi(l,e),ln(t,!0),t.tail===null&&t.tailMode==="hidden"&&!i.alternate&&!te)return ye(l),null}else 2*cl()-t.renderingStartTime>vi&&a!==536870912&&(l.flags|=128,n=!0,ln(t,!1),l.lanes=4194304);t.isBackwards?(i.sibling=l.child,l.child=i):(e=t.last,e!==null?e.sibling=i:l.child=i,t.last=i)}return t.tail!==null?(e=t.tail,t.rendering=e,t.tail=e.sibling,t.renderingStartTime=cl(),e.sibling=null,a=Te.current,C(Te,n?a&1|2:a&1),te&&Yl(l,t.treeForkCount),e):(ye(l),null);case 22:case 23:return dl(l),Qc(),t=l.memoizedState!==null,e!==null?e.memoizedState!==null!==t&&(l.flags|=8192):t&&(l.flags|=8192),t?(a&536870912)!==0&&(l.flags&128)===0&&(ye(l),l.subtreeFlags&6&&(l.flags|=8192)):ye(l),a=l.updateQueue,a!==null&&oi(l,a.retryQueue),a=null,e!==null&&e.memoizedState!==null&&e.memoizedState.cachePool!==null&&(a=e.memoizedState.cachePool.pool),t=null,l.memoizedState!==null&&l.memoizedState.cachePool!==null&&(t=l.memoizedState.cachePool.pool),t!==a&&(l.flags|=2048),e!==null&&T(Ra),null;case 24:return a=null,e!==null&&(a=e.memoizedState.cache),l.memoizedState.cache!==a&&(l.flags|=2048),Xl(Ae),ye(l),null;case 25:return null;case 30:return null}throw Error(r(156,l.tag))}function eh(e,l){switch(Tc(l),l.tag){case 1:return e=l.flags,e&65536?(l.flags=e&-65537|128,l):null;case 3:return Xl(Ae),ze(),e=l.flags,(e&65536)!==0&&(e&128)===0?(l.flags=e&-65537|128,l):null;case 26:case 27:case 5:return Sn(l),null;case 31:if(l.memoizedState!==null){if(dl(l),l.alternate===null)throw Error(r(340));Ma()}return e=l.flags,e&65536?(l.flags=e&-65537|128,l):null;case 13:if(dl(l),e=l.memoizedState,e!==null&&e.dehydrated!==null){if(l.alternate===null)throw Error(r(340));Ma()}return e=l.flags,e&65536?(l.flags=e&-65537|128,l):null;case 19:return T(Te),null;case 4:return ze(),null;case 10:return Xl(l.type),null;case 22:case 23:return dl(l),Qc(),e!==null&&T(Ra),e=l.flags,e&65536?(l.flags=e&-65537|128,l):null;case 24:return Xl(Ae),null;case 25:return null;default:return null}}function Lf(e,l){switch(Tc(l),l.tag){case 3:Xl(Ae),ze();break;case 26:case 27:case 5:Sn(l);break;case 4:ze();break;case 31:l.memoizedState!==null&&dl(l);break;case 13:dl(l);break;case 19:T(Te);break;case 10:Xl(l.type);break;case 22:case 23:dl(l),Qc(),e!==null&&T(Ra);break;case 24:Xl(Ae)}}function an(e,l){try{var a=l.updateQueue,t=a!==null?a.lastEffect:null;if(t!==null){var n=t.next;a=n;do{if((a.tag&e)===e){t=void 0;var i=a.create,u=a.inst;t=i(),u.destroy=t}a=a.next}while(a!==n)}}catch(s){oe(l,l.return,s)}}function fa(e,l,a){try{var t=l.updateQueue,n=t!==null?t.lastEffect:null;if(n!==null){var i=n.next;t=i;do{if((t.tag&e)===e){var u=t.inst,s=u.destroy;if(s!==void 0){u.destroy=void 0,n=l;var f=a,v=s;try{v()}catch(S){oe(n,f,S)}}}t=t.next}while(t!==i)}}catch(S){oe(l,l.return,S)}}function Zf(e){var l=e.updateQueue;if(l!==null){var a=e.stateNode;try{Ur(l,a)}catch(t){oe(e,e.return,t)}}}function wf(e,l,a){a.props=Ga(e.type,e.memoizedProps),a.state=e.memoizedState;try{a.componentWillUnmount()}catch(t){oe(e,l,t)}}function tn(e,l){try{var a=e.ref;if(a!==null){switch(e.tag){case 26:case 27:case 5:var t=e.stateNode;break;case 30:t=e.stateNode;break;default:t=e.stateNode}typeof a=="function"?e.refCleanup=a(t):a.current=t}}catch(n){oe(e,l,n)}}function Ul(e,l){var a=e.ref,t=e.refCleanup;if(a!==null)if(typeof t=="function")try{t()}catch(n){oe(e,l,n)}finally{e.refCleanup=null,e=e.alternate,e!=null&&(e.refCleanup=null)}else if(typeof a=="function")try{a(null)}catch(n){oe(e,l,n)}else a.current=null}function Vf(e){var l=e.type,a=e.memoizedProps,t=e.stateNode;try{e:switch(l){case"button":case"input":case"select":case"textarea":a.autoFocus&&t.focus();break e;case"img":a.src?t.src=a.src:a.srcSet&&(t.srcset=a.srcSet)}}catch(n){oe(e,e.return,n)}}function bu(e,l,a){try{var t=e.stateNode;Sh(t,e.type,a,l),t[We]=l}catch(n){oe(e,e.return,n)}}function kf(e){return e.tag===5||e.tag===3||e.tag===26||e.tag===27&&ga(e.type)||e.tag===4}function xu(e){e:for(;;){for(;e.sibling===null;){if(e.return===null||kf(e.return))return null;e=e.return}for(e.sibling.return=e.return,e=e.sibling;e.tag!==5&&e.tag!==6&&e.tag!==18;){if(e.tag===27&&ga(e.type)||e.flags&2||e.child===null||e.tag===4)continue e;e.child.return=e,e=e.child}if(!(e.flags&2))return e.stateNode}}function ju(e,l,a){var t=e.tag;if(t===5||t===6)e=e.stateNode,l?(a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a).insertBefore(e,l):(l=a.nodeType===9?a.body:a.nodeName==="HTML"?a.ownerDocument.body:a,l.appendChild(e),a=a._reactRootContainer,a!=null||l.onclick!==null||(l.onclick=Hl));else if(t!==4&&(t===27&&ga(e.type)&&(a=e.stateNode,l=null),e=e.child,e!==null))for(ju(e,l,a),e=e.sibling;e!==null;)ju(e,l,a),e=e.sibling}function di(e,l,a){var t=e.tag;if(t===5||t===6)e=e.stateNode,l?a.insertBefore(e,l):a.appendChild(e);else if(t!==4&&(t===27&&ga(e.type)&&(a=e.stateNode),e=e.child,e!==null))for(di(e,l,a),e=e.sibling;e!==null;)di(e,l,a),e=e.sibling}function Kf(e){var l=e.stateNode,a=e.memoizedProps;try{for(var t=e.type,n=l.attributes;n.length;)l.removeAttributeNode(n[0]);Ze(l,t,a),l[Ge]=e,l[We]=a}catch(i){oe(e,e.return,i)}}var Vl=!1,Me=!1,Su=!1,Jf=typeof WeakSet=="function"?WeakSet:Set,Be=null;function lh(e,l){if(e=e.containerInfo,Zu=Ci,e=ir(e),pc(e)){if("selectionStart"in e)var a={start:e.selectionStart,end:e.selectionEnd};else e:{a=(a=e.ownerDocument)&&a.defaultView||window;var t=a.getSelection&&a.getSelection();if(t&&t.rangeCount!==0){a=t.anchorNode;var n=t.anchorOffset,i=t.focusNode;t=t.focusOffset;try{a.nodeType,i.nodeType}catch{a=null;break e}var u=0,s=-1,f=-1,v=0,S=0,z=e,g=null;l:for(;;){for(var x;z!==a||n!==0&&z.nodeType!==3||(s=u+n),z!==i||t!==0&&z.nodeType!==3||(f=u+t),z.nodeType===3&&(u+=z.nodeValue.length),(x=z.firstChild)!==null;)g=z,z=x;for(;;){if(z===e)break l;if(g===a&&++v===n&&(s=u),g===i&&++S===t&&(f=u),(x=z.nextSibling)!==null)break;z=g,g=z.parentNode}z=x}a=s===-1||f===-1?null:{start:s,end:f}}else a=null}a=a||{start:0,end:0}}else a=null;for(wu={focusedElem:e,selectionRange:a},Ci=!1,Be=l;Be!==null;)if(l=Be,e=l.child,(l.subtreeFlags&1028)!==0&&e!==null)e.return=l,Be=e;else for(;Be!==null;){switch(l=Be,i=l.alternate,e=l.flags,l.tag){case 0:if((e&4)!==0&&(e=l.updateQueue,e=e!==null?e.events:null,e!==null))for(a=0;a<e.length;a++)n=e[a],n.ref.impl=n.nextImpl;break;case 11:case 15:break;case 1:if((e&1024)!==0&&i!==null){e=void 0,a=l,n=i.memoizedProps,i=i.memoizedState,t=a.stateNode;try{var Y=Ga(a.type,n);e=t.getSnapshotBeforeUpdate(Y,i),t.__reactInternalSnapshotBeforeUpdate=e}catch(V){oe(a,a.return,V)}}break;case 3:if((e&1024)!==0){if(e=l.stateNode.containerInfo,a=e.nodeType,a===9)Ku(e);else if(a===1)switch(e.nodeName){case"HEAD":case"HTML":case"BODY":Ku(e);break;default:e.textContent=""}}break;case 5:case 26:case 27:case 6:case 4:case 17:break;default:if((e&1024)!==0)throw Error(r(163))}if(e=l.sibling,e!==null){e.return=l.return,Be=e;break}Be=l.return}}function $f(e,l,a){var t=a.flags;switch(a.tag){case 0:case 11:case 15:Kl(e,a),t&4&&an(5,a);break;case 1:if(Kl(e,a),t&4)if(e=a.stateNode,l===null)try{e.componentDidMount()}catch(u){oe(a,a.return,u)}else{var n=Ga(a.type,l.memoizedProps);l=l.memoizedState;try{e.componentDidUpdate(n,l,e.__reactInternalSnapshotBeforeUpdate)}catch(u){oe(a,a.return,u)}}t&64&&Zf(a),t&512&&tn(a,a.return);break;case 3:if(Kl(e,a),t&64&&(e=a.updateQueue,e!==null)){if(l=null,a.child!==null)switch(a.child.tag){case 27:case 5:l=a.child.stateNode;break;case 1:l=a.child.stateNode}try{Ur(e,l)}catch(u){oe(a,a.return,u)}}break;case 27:l===null&&t&4&&Kf(a);case 26:case 5:Kl(e,a),l===null&&t&4&&Vf(a),t&512&&tn(a,a.return);break;case 12:Kl(e,a);break;case 31:Kl(e,a),t&4&&Pf(e,a);break;case 13:Kl(e,a),t&4&&If(e,a),t&64&&(e=a.memoizedState,e!==null&&(e=e.dehydrated,e!==null&&(a=fh.bind(null,a),Dh(e,a))));break;case 22:if(t=a.memoizedState!==null||Vl,!t){l=l!==null&&l.memoizedState!==null||Me,n=Vl;var i=Me;Vl=t,(Me=l)&&!i?Jl(e,a,(a.subtreeFlags&8772)!==0):Kl(e,a),Vl=n,Me=i}break;case 30:break;default:Kl(e,a)}}function Wf(e){var l=e.alternate;l!==null&&(e.alternate=null,Wf(l)),e.child=null,e.deletions=null,e.sibling=null,e.tag===5&&(l=e.stateNode,l!==null&&Pi(l)),e.stateNode=null,e.return=null,e.dependencies=null,e.memoizedProps=null,e.memoizedState=null,e.pendingProps=null,e.stateNode=null,e.updateQueue=null}var xe=null,Pe=!1;function kl(e,l,a){for(a=a.child;a!==null;)Ff(e,l,a),a=a.sibling}function Ff(e,l,a){if(ul&&typeof ul.onCommitFiberUnmount=="function")try{ul.onCommitFiberUnmount(Et,a)}catch{}switch(a.tag){case 26:Me||Ul(a,l),kl(e,l,a),a.memoizedState?a.memoizedState.count--:a.stateNode&&(a=a.stateNode,a.parentNode.removeChild(a));break;case 27:Me||Ul(a,l);var t=xe,n=Pe;ga(a.type)&&(xe=a.stateNode,Pe=!1),kl(e,l,a),mn(a.stateNode),xe=t,Pe=n;break;case 5:Me||Ul(a,l);case 6:if(t=xe,n=Pe,xe=null,kl(e,l,a),xe=t,Pe=n,xe!==null)if(Pe)try{(xe.nodeType===9?xe.body:xe.nodeName==="HTML"?xe.ownerDocument.body:xe).removeChild(a.stateNode)}catch(i){oe(a,l,i)}else try{xe.removeChild(a.stateNode)}catch(i){oe(a,l,i)}break;case 18:xe!==null&&(Pe?(e=xe,wo(e.nodeType===9?e.body:e.nodeName==="HTML"?e.ownerDocument.body:e,a.stateNode),zt(e)):wo(xe,a.stateNode));break;case 4:t=xe,n=Pe,xe=a.stateNode.containerInfo,Pe=!0,kl(e,l,a),xe=t,Pe=n;break;case 0:case 11:case 14:case 15:fa(2,a,l),Me||fa(4,a,l),kl(e,l,a);break;case 1:Me||(Ul(a,l),t=a.stateNode,typeof t.componentWillUnmount=="function"&&wf(a,l,t)),kl(e,l,a);break;case 21:kl(e,l,a);break;case 22:Me=(t=Me)||a.memoizedState!==null,kl(e,l,a),Me=t;break;default:kl(e,l,a)}}function Pf(e,l){if(l.memoizedState===null&&(e=l.alternate,e!==null&&(e=e.memoizedState,e!==null))){e=e.dehydrated;try{zt(e)}catch(a){oe(l,l.return,a)}}}function If(e,l){if(l.memoizedState===null&&(e=l.alternate,e!==null&&(e=e.memoizedState,e!==null&&(e=e.dehydrated,e!==null))))try{zt(e)}catch(a){oe(l,l.return,a)}}function ah(e){switch(e.tag){case 31:case 13:case 19:var l=e.stateNode;return l===null&&(l=e.stateNode=new Jf),l;case 22:return e=e.stateNode,l=e._retryCache,l===null&&(l=e._retryCache=new Jf),l;default:throw Error(r(435,e.tag))}}function mi(e,l){var a=ah(e);l.forEach(function(t){if(!a.has(t)){a.add(t);var n=oh.bind(null,e,t);t.then(n,n)}})}function Ie(e,l){var a=l.deletions;if(a!==null)for(var t=0;t<a.length;t++){var n=a[t],i=e,u=l,s=u;e:for(;s!==null;){switch(s.tag){case 27:if(ga(s.type)){xe=s.stateNode,Pe=!1;break e}break;case 5:xe=s.stateNode,Pe=!1;break e;case 3:case 4:xe=s.stateNode.containerInfo,Pe=!0;break e}s=s.return}if(xe===null)throw Error(r(160));Ff(i,u,n),xe=null,Pe=!1,i=n.alternate,i!==null&&(i.return=null),n.return=null}if(l.subtreeFlags&13886)for(l=l.child;l!==null;)eo(l,e),l=l.sibling}var Al=null;function eo(e,l){var a=e.alternate,t=e.flags;switch(e.tag){case 0:case 11:case 14:case 15:Ie(l,e),el(e),t&4&&(fa(3,e,e.return),an(3,e),fa(5,e,e.return));break;case 1:Ie(l,e),el(e),t&512&&(Me||a===null||Ul(a,a.return)),t&64&&Vl&&(e=e.updateQueue,e!==null&&(t=e.callbacks,t!==null&&(a=e.shared.hiddenCallbacks,e.shared.hiddenCallbacks=a===null?t:a.concat(t))));break;case 26:var n=Al;if(Ie(l,e),el(e),t&512&&(Me||a===null||Ul(a,a.return)),t&4){var i=a!==null?a.memoizedState:null;if(t=e.memoizedState,a===null)if(t===null)if(e.stateNode===null){e:{t=e.type,a=e.memoizedProps,n=n.ownerDocument||n;l:switch(t){case"title":i=n.getElementsByTagName("title")[0],(!i||i[Dt]||i[Ge]||i.namespaceURI==="http://www.w3.org/2000/svg"||i.hasAttribute("itemprop"))&&(i=n.createElement(t),n.head.insertBefore(i,n.querySelector("head > title"))),Ze(i,t,a),i[Ge]=e,He(i),t=i;break e;case"link":var u=ld("link","href",n).get(t+(a.href||""));if(u){for(var s=0;s<u.length;s++)if(i=u[s],i.getAttribute("href")===(a.href==null||a.href===""?null:a.href)&&i.getAttribute("rel")===(a.rel==null?null:a.rel)&&i.getAttribute("title")===(a.title==null?null:a.title)&&i.getAttribute("crossorigin")===(a.crossOrigin==null?null:a.crossOrigin)){u.splice(s,1);break l}}i=n.createElement(t),Ze(i,t,a),n.head.appendChild(i);break;case"meta":if(u=ld("meta","content",n).get(t+(a.content||""))){for(s=0;s<u.length;s++)if(i=u[s],i.getAttribute("content")===(a.content==null?null:""+a.content)&&i.getAttribute("name")===(a.name==null?null:a.name)&&i.getAttribute("property")===(a.property==null?null:a.property)&&i.getAttribute("http-equiv")===(a.httpEquiv==null?null:a.httpEquiv)&&i.getAttribute("charset")===(a.charSet==null?null:a.charSet)){u.splice(s,1);break l}}i=n.createElement(t),Ze(i,t,a),n.head.appendChild(i);break;default:throw Error(r(468,t))}i[Ge]=e,He(i),t=i}e.stateNode=t}else ad(n,e.type,e.stateNode);else e.stateNode=ed(n,t,e.memoizedProps);else i!==t?(i===null?a.stateNode!==null&&(a=a.stateNode,a.parentNode.removeChild(a)):i.count--,t===null?ad(n,e.type,e.stateNode):ed(n,t,e.memoizedProps)):t===null&&e.stateNode!==null&&bu(e,e.memoizedProps,a.memoizedProps)}break;case 27:Ie(l,e),el(e),t&512&&(Me||a===null||Ul(a,a.return)),a!==null&&t&4&&bu(e,e.memoizedProps,a.memoizedProps);break;case 5:if(Ie(l,e),el(e),t&512&&(Me||a===null||Ul(a,a.return)),e.flags&32){n=e.stateNode;try{Ja(n,"")}catch(Y){oe(e,e.return,Y)}}t&4&&e.stateNode!=null&&(n=e.memoizedProps,bu(e,n,a!==null?a.memoizedProps:n)),t&1024&&(Su=!0);break;case 6:if(Ie(l,e),el(e),t&4){if(e.stateNode===null)throw Error(r(162));t=e.memoizedProps,a=e.stateNode;try{a.nodeValue=t}catch(Y){oe(e,e.return,Y)}}break;case 3:if(Oi=null,n=Al,Al=Ei(l.containerInfo),Ie(l,e),Al=n,el(e),t&4&&a!==null&&a.memoizedState.isDehydrated)try{zt(l.containerInfo)}catch(Y){oe(e,e.return,Y)}Su&&(Su=!1,lo(e));break;case 4:t=Al,Al=Ei(e.stateNode.containerInfo),Ie(l,e),el(e),Al=t;break;case 12:Ie(l,e),el(e);break;case 31:Ie(l,e),el(e),t&4&&(t=e.updateQueue,t!==null&&(e.updateQueue=null,mi(e,t)));break;case 13:Ie(l,e),el(e),e.child.flags&8192&&e.memoizedState!==null!=(a!==null&&a.memoizedState!==null)&&(pi=cl()),t&4&&(t=e.updateQueue,t!==null&&(e.updateQueue=null,mi(e,t)));break;case 22:n=e.memoizedState!==null;var f=a!==null&&a.memoizedState!==null,v=Vl,S=Me;if(Vl=v||n,Me=S||f,Ie(l,e),Me=S,Vl=v,el(e),t&8192)e:for(l=e.stateNode,l._visibility=n?l._visibility&-2:l._visibility|1,n&&(a===null||f||Vl||Me||Xa(e)),a=null,l=e;;){if(l.tag===5||l.tag===26){if(a===null){f=a=l;try{if(i=f.stateNode,n)u=i.style,typeof u.setProperty=="function"?u.setProperty("display","none","important"):u.display="none";else{s=f.stateNode;var z=f.memoizedProps.style,g=z!=null&&z.hasOwnProperty("display")?z.display:null;s.style.display=g==null||typeof g=="boolean"?"":(""+g).trim()}}catch(Y){oe(f,f.return,Y)}}}else if(l.tag===6){if(a===null){f=l;try{f.stateNode.nodeValue=n?"":f.memoizedProps}catch(Y){oe(f,f.return,Y)}}}else if(l.tag===18){if(a===null){f=l;try{var x=f.stateNode;n?Vo(x,!0):Vo(f.stateNode,!1)}catch(Y){oe(f,f.return,Y)}}}else if((l.tag!==22&&l.tag!==23||l.memoizedState===null||l===e)&&l.child!==null){l.child.return=l,l=l.child;continue}if(l===e)break e;for(;l.sibling===null;){if(l.return===null||l.return===e)break e;a===l&&(a=null),l=l.return}a===l&&(a=null),l.sibling.return=l.return,l=l.sibling}t&4&&(t=e.updateQueue,t!==null&&(a=t.retryQueue,a!==null&&(t.retryQueue=null,mi(e,a))));break;case 19:Ie(l,e),el(e),t&4&&(t=e.updateQueue,t!==null&&(e.updateQueue=null,mi(e,t)));break;case 30:break;case 21:break;default:Ie(l,e),el(e)}}function el(e){var l=e.flags;if(l&2){try{for(var a,t=e.return;t!==null;){if(kf(t)){a=t;break}t=t.return}if(a==null)throw Error(r(160));switch(a.tag){case 27:var n=a.stateNode,i=xu(e);di(e,i,n);break;case 5:var u=a.stateNode;a.flags&32&&(Ja(u,""),a.flags&=-33);var s=xu(e);di(e,s,u);break;case 3:case 4:var f=a.stateNode.containerInfo,v=xu(e);ju(e,v,f);break;default:throw Error(r(161))}}catch(S){oe(e,e.return,S)}e.flags&=-3}l&4096&&(e.flags&=-4097)}function lo(e){if(e.subtreeFlags&1024)for(e=e.child;e!==null;){var l=e;lo(l),l.tag===5&&l.flags&1024&&l.stateNode.reset(),e=e.sibling}}function Kl(e,l){if(l.subtreeFlags&8772)for(l=l.child;l!==null;)$f(e,l.alternate,l),l=l.sibling}function Xa(e){for(e=e.child;e!==null;){var l=e;switch(l.tag){case 0:case 11:case 14:case 15:fa(4,l,l.return),Xa(l);break;case 1:Ul(l,l.return);var a=l.stateNode;typeof a.componentWillUnmount=="function"&&wf(l,l.return,a),Xa(l);break;case 27:mn(l.stateNode);case 26:case 5:Ul(l,l.return),Xa(l);break;case 22:l.memoizedState===null&&Xa(l);break;case 30:Xa(l);break;default:Xa(l)}e=e.sibling}}function Jl(e,l,a){for(a=a&&(l.subtreeFlags&8772)!==0,l=l.child;l!==null;){var t=l.alternate,n=e,i=l,u=i.flags;switch(i.tag){case 0:case 11:case 15:Jl(n,i,a),an(4,i);break;case 1:if(Jl(n,i,a),t=i,n=t.stateNode,typeof n.componentDidMount=="function")try{n.componentDidMount()}catch(v){oe(t,t.return,v)}if(t=i,n=t.updateQueue,n!==null){var s=t.stateNode;try{var f=n.shared.hiddenCallbacks;if(f!==null)for(n.shared.hiddenCallbacks=null,n=0;n<f.length;n++)Mr(f[n],s)}catch(v){oe(t,t.return,v)}}a&&u&64&&Zf(i),tn(i,i.return);break;case 27:Kf(i);case 26:case 5:Jl(n,i,a),a&&t===null&&u&4&&Vf(i),tn(i,i.return);break;case 12:Jl(n,i,a);break;case 31:Jl(n,i,a),a&&u&4&&Pf(n,i);break;case 13:Jl(n,i,a),a&&u&4&&If(n,i);break;case 22:i.memoizedState===null&&Jl(n,i,a),tn(i,i.return);break;case 30:break;default:Jl(n,i,a)}l=l.sibling}}function Nu(e,l){var a=null;e!==null&&e.memoizedState!==null&&e.memoizedState.cachePool!==null&&(a=e.memoizedState.cachePool.pool),e=null,l.memoizedState!==null&&l.memoizedState.cachePool!==null&&(e=l.memoizedState.cachePool.pool),e!==a&&(e!=null&&e.refCount++,a!=null&&Zt(a))}function _u(e,l){e=null,l.alternate!==null&&(e=l.alternate.memoizedState.cache),l=l.memoizedState.cache,l!==e&&(l.refCount++,e!=null&&Zt(e))}function Ol(e,l,a,t){if(l.subtreeFlags&10256)for(l=l.child;l!==null;)ao(e,l,a,t),l=l.sibling}function ao(e,l,a,t){var n=l.flags;switch(l.tag){case 0:case 11:case 15:Ol(e,l,a,t),n&2048&&an(9,l);break;case 1:Ol(e,l,a,t);break;case 3:Ol(e,l,a,t),n&2048&&(e=null,l.alternate!==null&&(e=l.alternate.memoizedState.cache),l=l.memoizedState.cache,l!==e&&(l.refCount++,e!=null&&Zt(e)));break;case 12:if(n&2048){Ol(e,l,a,t),e=l.stateNode;try{var i=l.memoizedProps,u=i.id,s=i.onPostCommit;typeof s=="function"&&s(u,l.alternate===null?"mount":"update",e.passiveEffectDuration,-0)}catch(f){oe(l,l.return,f)}}else Ol(e,l,a,t);break;case 31:Ol(e,l,a,t);break;case 13:Ol(e,l,a,t);break;case 23:break;case 22:i=l.stateNode,u=l.alternate,l.memoizedState!==null?i._visibility&2?Ol(e,l,a,t):nn(e,l):i._visibility&2?Ol(e,l,a,t):(i._visibility|=2,ht(e,l,a,t,(l.subtreeFlags&10256)!==0||!1)),n&2048&&Nu(u,l);break;case 24:Ol(e,l,a,t),n&2048&&_u(l.alternate,l);break;default:Ol(e,l,a,t)}}function ht(e,l,a,t,n){for(n=n&&((l.subtreeFlags&10256)!==0||!1),l=l.child;l!==null;){var i=e,u=l,s=a,f=t,v=u.flags;switch(u.tag){case 0:case 11:case 15:ht(i,u,s,f,n),an(8,u);break;case 23:break;case 22:var S=u.stateNode;u.memoizedState!==null?S._visibility&2?ht(i,u,s,f,n):nn(i,u):(S._visibility|=2,ht(i,u,s,f,n)),n&&v&2048&&Nu(u.alternate,u);break;case 24:ht(i,u,s,f,n),n&&v&2048&&_u(u.alternate,u);break;default:ht(i,u,s,f,n)}l=l.sibling}}function nn(e,l){if(l.subtreeFlags&10256)for(l=l.child;l!==null;){var a=e,t=l,n=t.flags;switch(t.tag){case 22:nn(a,t),n&2048&&Nu(t.alternate,t);break;case 24:nn(a,t),n&2048&&_u(t.alternate,t);break;default:nn(a,t)}l=l.sibling}}var cn=8192;function pt(e,l,a){if(e.subtreeFlags&cn)for(e=e.child;e!==null;)to(e,l,a),e=e.sibling}function to(e,l,a){switch(e.tag){case 26:pt(e,l,a),e.flags&cn&&e.memoizedState!==null&&Lh(a,Al,e.memoizedState,e.memoizedProps);break;case 5:pt(e,l,a);break;case 3:case 4:var t=Al;Al=Ei(e.stateNode.containerInfo),pt(e,l,a),Al=t;break;case 22:e.memoizedState===null&&(t=e.alternate,t!==null&&t.memoizedState!==null?(t=cn,cn=16777216,pt(e,l,a),cn=t):pt(e,l,a));break;default:pt(e,l,a)}}function no(e){var l=e.alternate;if(l!==null&&(e=l.child,e!==null)){l.child=null;do l=e.sibling,e.sibling=null,e=l;while(e!==null)}}function un(e){var l=e.deletions;if((e.flags&16)!==0){if(l!==null)for(var a=0;a<l.length;a++){var t=l[a];Be=t,co(t,e)}no(e)}if(e.subtreeFlags&10256)for(e=e.child;e!==null;)io(e),e=e.sibling}function io(e){switch(e.tag){case 0:case 11:case 15:un(e),e.flags&2048&&fa(9,e,e.return);break;case 3:un(e);break;case 12:un(e);break;case 22:var l=e.stateNode;e.memoizedState!==null&&l._visibility&2&&(e.return===null||e.return.tag!==13)?(l._visibility&=-3,hi(e)):un(e);break;default:un(e)}}function hi(e){var l=e.deletions;if((e.flags&16)!==0){if(l!==null)for(var a=0;a<l.length;a++){var t=l[a];Be=t,co(t,e)}no(e)}for(e=e.child;e!==null;){switch(l=e,l.tag){case 0:case 11:case 15:fa(8,l,l.return),hi(l);break;case 22:a=l.stateNode,a._visibility&2&&(a._visibility&=-3,hi(l));break;default:hi(l)}e=e.sibling}}function co(e,l){for(;Be!==null;){var a=Be;switch(a.tag){case 0:case 11:case 15:fa(8,a,l);break;case 23:case 22:if(a.memoizedState!==null&&a.memoizedState.cachePool!==null){var t=a.memoizedState.cachePool.pool;t!=null&&t.refCount++}break;case 24:Zt(a.memoizedState.cache)}if(t=a.child,t!==null)t.return=a,Be=t;else e:for(a=e;Be!==null;){t=Be;var n=t.sibling,i=t.return;if(Wf(t),t===a){Be=null;break e}if(n!==null){n.return=i,Be=n;break e}Be=i}}}var th={getCacheForType:function(e){var l=Qe(Ae),a=l.data.get(e);return a===void 0&&(a=e(),l.data.set(e,a)),a},cacheSignal:function(){return Qe(Ae).controller.signal}},nh=typeof WeakMap=="function"?WeakMap:Map,ce=0,pe=null,I=null,le=0,fe=0,ml=null,oa=!1,vt=!1,zu=!1,$l=0,Ne=0,da=0,Qa=0,Tu=0,hl=0,gt=0,sn=null,ll=null,Eu=!1,pi=0,uo=0,vi=1/0,gi=null,ma=null,Ce=0,ha=null,yt=null,Wl=0,Au=0,Ou=null,so=null,rn=0,Du=null;function pl(){return(ce&2)!==0&&le!==0?le&-le:N.T!==null?Bu():Ns()}function ro(){if(hl===0)if((le&536870912)===0||te){var e=zn;zn<<=1,(zn&3932160)===0&&(zn=262144),hl=e}else hl=536870912;return e=ol.current,e!==null&&(e.flags|=32),hl}function al(e,l,a){(e===pe&&(fe===2||fe===9)||e.cancelPendingCommit!==null)&&(bt(e,0),pa(e,le,hl,!1)),Ot(e,a),((ce&2)===0||e!==pe)&&(e===pe&&((ce&2)===0&&(Qa|=a),Ne===4&&pa(e,le,hl,!1)),Cl(e))}function fo(e,l,a){if((ce&6)!==0)throw Error(r(327));var t=!a&&(l&127)===0&&(l&e.expiredLanes)===0||At(e,l),n=t?uh(e,l):Uu(e,l,!0),i=t;do{if(n===0){vt&&!t&&pa(e,l,0,!1);break}else{if(a=e.current.alternate,i&&!ih(a)){n=Uu(e,l,!1),i=!1;continue}if(n===2){if(i=l,e.errorRecoveryDisabledLanes&i)var u=0;else u=e.pendingLanes&-536870913,u=u!==0?u:u&536870912?536870912:0;if(u!==0){l=u;e:{var s=e;n=sn;var f=s.current.memoizedState.isDehydrated;if(f&&(bt(s,u).flags|=256),u=Uu(s,u,!1),u!==2){if(zu&&!f){s.errorRecoveryDisabledLanes|=i,Qa|=i,n=4;break e}i=ll,ll=n,i!==null&&(ll===null?ll=i:ll.push.apply(ll,i))}n=u}if(i=!1,n!==2)continue}}if(n===1){bt(e,0),pa(e,l,0,!0);break}e:{switch(t=e,i=n,i){case 0:case 1:throw Error(r(345));case 4:if((l&4194048)!==l)break;case 6:pa(t,l,hl,!oa);break e;case 2:ll=null;break;case 3:case 5:break;default:throw Error(r(329))}if((l&62914560)===l&&(n=pi+300-cl(),10<n)){if(pa(t,l,hl,!oa),En(t,0,!0)!==0)break e;Wl=l,t.timeoutHandle=Lo(oo.bind(null,t,a,ll,gi,Eu,l,hl,Qa,gt,oa,i,"Throttled",-0,0),n);break e}oo(t,a,ll,gi,Eu,l,hl,Qa,gt,oa,i,null,-0,0)}}break}while(!0);Cl(e)}function oo(e,l,a,t,n,i,u,s,f,v,S,z,g,x){if(e.timeoutHandle=-1,z=l.subtreeFlags,z&8192||(z&16785408)===16785408){z={stylesheets:null,count:0,imgCount:0,imgBytes:0,suspenseyImages:[],waitingForImages:!0,waitingForViewTransition:!1,unsuspend:Hl},to(l,i,z);var Y=(i&62914560)===i?pi-cl():(i&4194048)===i?uo-cl():0;if(Y=Zh(z,Y),Y!==null){Wl=i,e.cancelPendingCommit=Y(xo.bind(null,e,l,i,a,t,n,u,s,f,S,z,null,g,x)),pa(e,i,u,!v);return}}xo(e,l,i,a,t,n,u,s,f)}function ih(e){for(var l=e;;){var a=l.tag;if((a===0||a===11||a===15)&&l.flags&16384&&(a=l.updateQueue,a!==null&&(a=a.stores,a!==null)))for(var t=0;t<a.length;t++){var n=a[t],i=n.getSnapshot;n=n.value;try{if(!rl(i(),n))return!1}catch{return!1}}if(a=l.child,l.subtreeFlags&16384&&a!==null)a.return=l,l=a;else{if(l===e)break;for(;l.sibling===null;){if(l.return===null||l.return===e)return!0;l=l.return}l.sibling.return=l.return,l=l.sibling}}return!0}function pa(e,l,a,t){l&=~Tu,l&=~Qa,e.suspendedLanes|=l,e.pingedLanes&=~l,t&&(e.warmLanes|=l),t=e.expirationTimes;for(var n=l;0<n;){var i=31-sl(n),u=1<<i;t[i]=-1,n&=~u}a!==0&&xs(e,a,l)}function yi(){return(ce&6)===0?(fn(0),!1):!0}function Mu(){if(I!==null){if(fe===0)var e=I.return;else e=I,Gl=Ua=null,Kc(e),rt=null,Vt=0,e=I;for(;e!==null;)Lf(e.alternate,e),e=e.return;I=null}}function bt(e,l){var a=e.timeoutHandle;a!==-1&&(e.timeoutHandle=-1,zh(a)),a=e.cancelPendingCommit,a!==null&&(e.cancelPendingCommit=null,a()),Wl=0,Mu(),pe=e,I=a=ql(e.current,null),le=l,fe=0,ml=null,oa=!1,vt=At(e,l),zu=!1,gt=hl=Tu=Qa=da=Ne=0,ll=sn=null,Eu=!1,(l&8)!==0&&(l|=l&32);var t=e.entangledLanes;if(t!==0)for(e=e.entanglements,t&=l;0<t;){var n=31-sl(t),i=1<<n;l|=e[n],t&=~i}return $l=l,Gn(),a}function mo(e,l){$=null,N.H=It,l===st||l===Kn?(l=Er(),fe=3):l===Hc?(l=Er(),fe=4):fe=l===ru?8:l!==null&&typeof l=="object"&&typeof l.then=="function"?6:1,ml=l,I===null&&(Ne=1,ui(e,bl(l,e.current)))}function ho(){var e=ol.current;return e===null?!0:(le&4194048)===le?Nl===null:(le&62914560)===le||(le&536870912)!==0?e===Nl:!1}function po(){var e=N.H;return N.H=It,e===null?It:e}function vo(){var e=N.A;return N.A=th,e}function bi(){Ne=4,oa||(le&4194048)!==le&&ol.current!==null||(vt=!0),(da&134217727)===0&&(Qa&134217727)===0||pe===null||pa(pe,le,hl,!1)}function Uu(e,l,a){var t=ce;ce|=2;var n=po(),i=vo();(pe!==e||le!==l)&&(gi=null,bt(e,l)),l=!1;var u=Ne;e:do try{if(fe!==0&&I!==null){var s=I,f=ml;switch(fe){case 8:Mu(),u=6;break e;case 3:case 2:case 9:case 6:ol.current===null&&(l=!0);var v=fe;if(fe=0,ml=null,xt(e,s,f,v),a&&vt){u=0;break e}break;default:v=fe,fe=0,ml=null,xt(e,s,f,v)}}ch(),u=Ne;break}catch(S){mo(e,S)}while(!0);return l&&e.shellSuspendCounter++,Gl=Ua=null,ce=t,N.H=n,N.A=i,I===null&&(pe=null,le=0,Gn()),u}function ch(){for(;I!==null;)go(I)}function uh(e,l){var a=ce;ce|=2;var t=po(),n=vo();pe!==e||le!==l?(gi=null,vi=cl()+500,bt(e,l)):vt=At(e,l);e:do try{if(fe!==0&&I!==null){l=I;var i=ml;l:switch(fe){case 1:fe=0,ml=null,xt(e,l,i,1);break;case 2:case 9:if(zr(i)){fe=0,ml=null,yo(l);break}l=function(){fe!==2&&fe!==9||pe!==e||(fe=7),Cl(e)},i.then(l,l);break e;case 3:fe=7;break e;case 4:fe=5;break e;case 7:zr(i)?(fe=0,ml=null,yo(l)):(fe=0,ml=null,xt(e,l,i,7));break;case 5:var u=null;switch(I.tag){case 26:u=I.memoizedState;case 5:case 27:var s=I;if(u?td(u):s.stateNode.complete){fe=0,ml=null;var f=s.sibling;if(f!==null)I=f;else{var v=s.return;v!==null?(I=v,xi(v)):I=null}break l}}fe=0,ml=null,xt(e,l,i,5);break;case 6:fe=0,ml=null,xt(e,l,i,6);break;case 8:Mu(),Ne=6;break e;default:throw Error(r(462))}}sh();break}catch(S){mo(e,S)}while(!0);return Gl=Ua=null,N.H=t,N.A=n,ce=a,I!==null?0:(pe=null,le=0,Gn(),Ne)}function sh(){for(;I!==null&&!Md();)go(I)}function go(e){var l=Xf(e.alternate,e,$l);e.memoizedProps=e.pendingProps,l===null?xi(e):I=l}function yo(e){var l=e,a=l.alternate;switch(l.tag){case 15:case 0:l=Rf(a,l,l.pendingProps,l.type,void 0,le);break;case 11:l=Rf(a,l,l.pendingProps,l.type.render,l.ref,le);break;case 5:Kc(l);default:Lf(a,l),l=I=hr(l,$l),l=Xf(a,l,$l)}e.memoizedProps=e.pendingProps,l===null?xi(e):I=l}function xt(e,l,a,t){Gl=Ua=null,Kc(l),rt=null,Vt=0;var n=l.return;try{if(Wm(e,n,l,a,le)){Ne=1,ui(e,bl(a,e.current)),I=null;return}}catch(i){if(n!==null)throw I=n,i;Ne=1,ui(e,bl(a,e.current)),I=null;return}l.flags&32768?(te||t===1?e=!0:vt||(le&536870912)!==0?e=!1:(oa=e=!0,(t===2||t===9||t===3||t===6)&&(t=ol.current,t!==null&&t.tag===13&&(t.flags|=16384))),bo(l,e)):xi(l)}function xi(e){var l=e;do{if((l.flags&32768)!==0){bo(l,oa);return}e=l.return;var a=Im(l.alternate,l,$l);if(a!==null){I=a;return}if(l=l.sibling,l!==null){I=l;return}I=l=e}while(l!==null);Ne===0&&(Ne=5)}function bo(e,l){do{var a=eh(e.alternate,e);if(a!==null){a.flags&=32767,I=a;return}if(a=e.return,a!==null&&(a.flags|=32768,a.subtreeFlags=0,a.deletions=null),!l&&(e=e.sibling,e!==null)){I=e;return}I=e=a}while(e!==null);Ne=6,I=null}function xo(e,l,a,t,n,i,u,s,f){e.cancelPendingCommit=null;do ji();while(Ce!==0);if((ce&6)!==0)throw Error(r(327));if(l!==null){if(l===e.current)throw Error(r(177));if(i=l.lanes|l.childLanes,i|=xc,Qd(e,a,i,u,s,f),e===pe&&(I=pe=null,le=0),yt=l,ha=e,Wl=a,Au=i,Ou=n,so=t,(l.subtreeFlags&10256)!==0||(l.flags&10256)!==0?(e.callbackNode=null,e.callbackPriority=0,dh(Nn,function(){return zo(),null})):(e.callbackNode=null,e.callbackPriority=0),t=(l.flags&13878)!==0,(l.subtreeFlags&13878)!==0||t){t=N.T,N.T=null,n=R.p,R.p=2,u=ce,ce|=4;try{lh(e,l,a)}finally{ce=u,R.p=n,N.T=t}}Ce=1,jo(),So(),No()}}function jo(){if(Ce===1){Ce=0;var e=ha,l=yt,a=(l.flags&13878)!==0;if((l.subtreeFlags&13878)!==0||a){a=N.T,N.T=null;var t=R.p;R.p=2;var n=ce;ce|=4;try{eo(l,e);var i=wu,u=ir(e.containerInfo),s=i.focusedElem,f=i.selectionRange;if(u!==s&&s&&s.ownerDocument&&nr(s.ownerDocument.documentElement,s)){if(f!==null&&pc(s)){var v=f.start,S=f.end;if(S===void 0&&(S=v),"selectionStart"in s)s.selectionStart=v,s.selectionEnd=Math.min(S,s.value.length);else{var z=s.ownerDocument||document,g=z&&z.defaultView||window;if(g.getSelection){var x=g.getSelection(),Y=s.textContent.length,V=Math.min(f.start,Y),he=f.end===void 0?V:Math.min(f.end,Y);!x.extend&&V>he&&(u=he,he=V,V=u);var m=tr(s,V),o=tr(s,he);if(m&&o&&(x.rangeCount!==1||x.anchorNode!==m.node||x.anchorOffset!==m.offset||x.focusNode!==o.node||x.focusOffset!==o.offset)){var p=z.createRange();p.setStart(m.node,m.offset),x.removeAllRanges(),V>he?(x.addRange(p),x.extend(o.node,o.offset)):(p.setEnd(o.node,o.offset),x.addRange(p))}}}}for(z=[],x=s;x=x.parentNode;)x.nodeType===1&&z.push({element:x,left:x.scrollLeft,top:x.scrollTop});for(typeof s.focus=="function"&&s.focus(),s=0;s<z.length;s++){var _=z[s];_.element.scrollLeft=_.left,_.element.scrollTop=_.top}}Ci=!!Zu,wu=Zu=null}finally{ce=n,R.p=t,N.T=a}}e.current=l,Ce=2}}function So(){if(Ce===2){Ce=0;var e=ha,l=yt,a=(l.flags&8772)!==0;if((l.subtreeFlags&8772)!==0||a){a=N.T,N.T=null;var t=R.p;R.p=2;var n=ce;ce|=4;try{$f(e,l.alternate,l)}finally{ce=n,R.p=t,N.T=a}}Ce=3}}function No(){if(Ce===4||Ce===3){Ce=0,Ud();var e=ha,l=yt,a=Wl,t=so;(l.subtreeFlags&10256)!==0||(l.flags&10256)!==0?Ce=5:(Ce=0,yt=ha=null,_o(e,e.pendingLanes));var n=e.pendingLanes;if(n===0&&(ma=null),Wi(a),l=l.stateNode,ul&&typeof ul.onCommitFiberRoot=="function")try{ul.onCommitFiberRoot(Et,l,void 0,(l.current.flags&128)===128)}catch{}if(t!==null){l=N.T,n=R.p,R.p=2,N.T=null;try{for(var i=e.onRecoverableError,u=0;u<t.length;u++){var s=t[u];i(s.value,{componentStack:s.stack})}}finally{N.T=l,R.p=n}}(Wl&3)!==0&&ji(),Cl(e),n=e.pendingLanes,(a&261930)!==0&&(n&42)!==0?e===Du?rn++:(rn=0,Du=e):rn=0,fn(0)}}function _o(e,l){(e.pooledCacheLanes&=l)===0&&(l=e.pooledCache,l!=null&&(e.pooledCache=null,Zt(l)))}function ji(){return jo(),So(),No(),zo()}function zo(){if(Ce!==5)return!1;var e=ha,l=Au;Au=0;var a=Wi(Wl),t=N.T,n=R.p;try{R.p=32>a?32:a,N.T=null,a=Ou,Ou=null;var i=ha,u=Wl;if(Ce=0,yt=ha=null,Wl=0,(ce&6)!==0)throw Error(r(331));var s=ce;if(ce|=4,io(i.current),ao(i,i.current,u,a),ce=s,fn(0,!1),ul&&typeof ul.onPostCommitFiberRoot=="function")try{ul.onPostCommitFiberRoot(Et,i)}catch{}return!0}finally{R.p=n,N.T=t,_o(e,l)}}function To(e,l,a){l=bl(a,l),l=su(e.stateNode,l,2),e=ua(e,l,2),e!==null&&(Ot(e,2),Cl(e))}function oe(e,l,a){if(e.tag===3)To(e,e,a);else for(;l!==null;){if(l.tag===3){To(l,e,a);break}else if(l.tag===1){var t=l.stateNode;if(typeof l.type.getDerivedStateFromError=="function"||typeof t.componentDidCatch=="function"&&(ma===null||!ma.has(t))){e=bl(a,e),a=Tf(2),t=ua(l,a,2),t!==null&&(Ef(a,t,l,e),Ot(t,2),Cl(t));break}}l=l.return}}function Cu(e,l,a){var t=e.pingCache;if(t===null){t=e.pingCache=new nh;var n=new Set;t.set(l,n)}else n=t.get(l),n===void 0&&(n=new Set,t.set(l,n));n.has(a)||(zu=!0,n.add(a),e=rh.bind(null,e,l,a),l.then(e,e))}function rh(e,l,a){var t=e.pingCache;t!==null&&t.delete(l),e.pingedLanes|=e.suspendedLanes&a,e.warmLanes&=~a,pe===e&&(le&a)===a&&(Ne===4||Ne===3&&(le&62914560)===le&&300>cl()-pi?(ce&2)===0&&bt(e,0):Tu|=a,gt===le&&(gt=0)),Cl(e)}function Eo(e,l){l===0&&(l=bs()),e=Oa(e,l),e!==null&&(Ot(e,l),Cl(e))}function fh(e){var l=e.memoizedState,a=0;l!==null&&(a=l.retryLane),Eo(e,a)}function oh(e,l){var a=0;switch(e.tag){case 31:case 13:var t=e.stateNode,n=e.memoizedState;n!==null&&(a=n.retryLane);break;case 19:t=e.stateNode;break;case 22:t=e.stateNode._retryCache;break;default:throw Error(r(314))}t!==null&&t.delete(l),Eo(e,a)}function dh(e,l){return ki(e,l)}var Si=null,jt=null,Ru=!1,Ni=!1,Hu=!1,va=0;function Cl(e){e!==jt&&e.next===null&&(jt===null?Si=jt=e:jt=jt.next=e),Ni=!0,Ru||(Ru=!0,hh())}function fn(e,l){if(!Hu&&Ni){Hu=!0;do for(var a=!1,t=Si;t!==null;){if(e!==0){var n=t.pendingLanes;if(n===0)var i=0;else{var u=t.suspendedLanes,s=t.pingedLanes;i=(1<<31-sl(42|e)+1)-1,i&=n&~(u&~s),i=i&201326741?i&201326741|1:i?i|2:0}i!==0&&(a=!0,Mo(t,i))}else i=le,i=En(t,t===pe?i:0,t.cancelPendingCommit!==null||t.timeoutHandle!==-1),(i&3)===0||At(t,i)||(a=!0,Mo(t,i));t=t.next}while(a);Hu=!1}}function mh(){Ao()}function Ao(){Ni=Ru=!1;var e=0;va!==0&&_h()&&(e=va);for(var l=cl(),a=null,t=Si;t!==null;){var n=t.next,i=Oo(t,l);i===0?(t.next=null,a===null?Si=n:a.next=n,n===null&&(jt=a)):(a=t,(e!==0||(i&3)!==0)&&(Ni=!0)),t=n}Ce!==0&&Ce!==5||fn(e),va!==0&&(va=0)}function Oo(e,l){for(var a=e.suspendedLanes,t=e.pingedLanes,n=e.expirationTimes,i=e.pendingLanes&-62914561;0<i;){var u=31-sl(i),s=1<<u,f=n[u];f===-1?((s&a)===0||(s&t)!==0)&&(n[u]=Xd(s,l)):f<=l&&(e.expiredLanes|=s),i&=~s}if(l=pe,a=le,a=En(e,e===l?a:0,e.cancelPendingCommit!==null||e.timeoutHandle!==-1),t=e.callbackNode,a===0||e===l&&(fe===2||fe===9)||e.cancelPendingCommit!==null)return t!==null&&t!==null&&Ki(t),e.callbackNode=null,e.callbackPriority=0;if((a&3)===0||At(e,a)){if(l=a&-a,l===e.callbackPriority)return l;switch(t!==null&&Ki(t),Wi(a)){case 2:case 8:a=gs;break;case 32:a=Nn;break;case 268435456:a=ys;break;default:a=Nn}return t=Do.bind(null,e),a=ki(a,t),e.callbackPriority=l,e.callbackNode=a,l}return t!==null&&t!==null&&Ki(t),e.callbackPriority=2,e.callbackNode=null,2}function Do(e,l){if(Ce!==0&&Ce!==5)return e.callbackNode=null,e.callbackPriority=0,null;var a=e.callbackNode;if(ji()&&e.callbackNode!==a)return null;var t=le;return t=En(e,e===pe?t:0,e.cancelPendingCommit!==null||e.timeoutHandle!==-1),t===0?null:(fo(e,t,l),Oo(e,cl()),e.callbackNode!=null&&e.callbackNode===a?Do.bind(null,e):null)}function Mo(e,l){if(ji())return null;fo(e,l,!0)}function hh(){Th(function(){(ce&6)!==0?ki(vs,mh):Ao()})}function Bu(){if(va===0){var e=ct;e===0&&(e=_n,_n<<=1,(_n&261888)===0&&(_n=256)),va=e}return va}function Uo(e){return e==null||typeof e=="symbol"||typeof e=="boolean"?null:typeof e=="function"?e:Mn(""+e)}function Co(e,l){var a=l.ownerDocument.createElement("input");return a.name=l.name,a.value=l.value,e.id&&a.setAttribute("form",e.id),l.parentNode.insertBefore(a,l),e=new FormData(e),a.parentNode.removeChild(a),e}function ph(e,l,a,t,n){if(l==="submit"&&a&&a.stateNode===n){var i=Uo((n[We]||null).action),u=t.submitter;u&&(l=(l=u[We]||null)?Uo(l.formAction):u.getAttribute("formAction"),l!==null&&(i=l,u=null));var s=new Hn("action","action",null,t,n);e.push({event:s,listeners:[{instance:null,listener:function(){if(t.defaultPrevented){if(va!==0){var f=u?Co(n,u):new FormData(n);au(a,{pending:!0,data:f,method:n.method,action:i},null,f)}}else typeof i=="function"&&(s.preventDefault(),f=u?Co(n,u):new FormData(n),au(a,{pending:!0,data:f,method:n.method,action:i},i,f))},currentTarget:n}]})}}for(var qu=0;qu<bc.length;qu++){var Yu=bc[qu],vh=Yu.toLowerCase(),gh=Yu[0].toUpperCase()+Yu.slice(1);El(vh,"on"+gh)}El(sr,"onAnimationEnd"),El(rr,"onAnimationIteration"),El(fr,"onAnimationStart"),El("dblclick","onDoubleClick"),El("focusin","onFocus"),El("focusout","onBlur"),El(Cm,"onTransitionRun"),El(Rm,"onTransitionStart"),El(Hm,"onTransitionCancel"),El(or,"onTransitionEnd"),ka("onMouseEnter",["mouseout","mouseover"]),ka("onMouseLeave",["mouseout","mouseover"]),ka("onPointerEnter",["pointerout","pointerover"]),ka("onPointerLeave",["pointerout","pointerover"]),za("onChange","change click focusin focusout input keydown keyup selectionchange".split(" ")),za("onSelect","focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(" ")),za("onBeforeInput",["compositionend","keypress","textInput","paste"]),za("onCompositionEnd","compositionend focusout keydown keypress keyup mousedown".split(" ")),za("onCompositionStart","compositionstart focusout keydown keypress keyup mousedown".split(" ")),za("onCompositionUpdate","compositionupdate focusout keydown keypress keyup mousedown".split(" "));var on="abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(" "),yh=new Set("beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(on));function Ro(e,l){l=(l&4)!==0;for(var a=0;a<e.length;a++){var t=e[a],n=t.event;t=t.listeners;e:{var i=void 0;if(l)for(var u=t.length-1;0<=u;u--){var s=t[u],f=s.instance,v=s.currentTarget;if(s=s.listener,f!==i&&n.isPropagationStopped())break e;i=s,n.currentTarget=v;try{i(n)}catch(S){Yn(S)}n.currentTarget=null,i=f}else for(u=0;u<t.length;u++){if(s=t[u],f=s.instance,v=s.currentTarget,s=s.listener,f!==i&&n.isPropagationStopped())break e;i=s,n.currentTarget=v;try{i(n)}catch(S){Yn(S)}n.currentTarget=null,i=f}}}}function ee(e,l){var a=l[Fi];a===void 0&&(a=l[Fi]=new Set);var t=e+"__bubble";a.has(t)||(Ho(l,e,2,!1),a.add(t))}function Gu(e,l,a){var t=0;l&&(t|=4),Ho(a,e,t,l)}var _i="_reactListening"+Math.random().toString(36).slice(2);function Xu(e){if(!e[_i]){e[_i]=!0,Ts.forEach(function(a){a!=="selectionchange"&&(yh.has(a)||Gu(a,!1,e),Gu(a,!0,e))});var l=e.nodeType===9?e:e.ownerDocument;l===null||l[_i]||(l[_i]=!0,Gu("selectionchange",!1,l))}}function Ho(e,l,a,t){switch(fd(l)){case 2:var n=kh;break;case 8:n=Kh;break;default:n=ls}a=n.bind(null,l,a,e),n=void 0,!cc||l!=="touchstart"&&l!=="touchmove"&&l!=="wheel"||(n=!0),t?n!==void 0?e.addEventListener(l,a,{capture:!0,passive:n}):e.addEventListener(l,a,!0):n!==void 0?e.addEventListener(l,a,{passive:n}):e.addEventListener(l,a,!1)}function Qu(e,l,a,t,n){var i=t;if((l&1)===0&&(l&2)===0&&t!==null)e:for(;;){if(t===null)return;var u=t.tag;if(u===3||u===4){var s=t.stateNode.containerInfo;if(s===n)break;if(u===4)for(u=t.return;u!==null;){var f=u.tag;if((f===3||f===4)&&u.stateNode.containerInfo===n)return;u=u.return}for(;s!==null;){if(u=Za(s),u===null)return;if(f=u.tag,f===5||f===6||f===26||f===27){t=i=u;continue e}s=s.parentNode}}t=t.return}Ys(function(){var v=i,S=nc(a),z=[];e:{var g=dr.get(e);if(g!==void 0){var x=Hn,Y=e;switch(e){case"keypress":if(Cn(a)===0)break e;case"keydown":case"keyup":x=om;break;case"focusin":Y="focus",x=fc;break;case"focusout":Y="blur",x=fc;break;case"beforeblur":case"afterblur":x=fc;break;case"click":if(a.button===2)break e;case"auxclick":case"dblclick":case"mousedown":case"mousemove":case"mouseup":case"mouseout":case"mouseover":case"contextmenu":x=Qs;break;case"drag":case"dragend":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"dragstart":case"drop":x=Id;break;case"touchcancel":case"touchend":case"touchmove":case"touchstart":x=hm;break;case sr:case rr:case fr:x=am;break;case or:x=vm;break;case"scroll":case"scrollend":x=Fd;break;case"wheel":x=ym;break;case"copy":case"cut":case"paste":x=nm;break;case"gotpointercapture":case"lostpointercapture":case"pointercancel":case"pointerdown":case"pointermove":case"pointerout":case"pointerover":case"pointerup":x=Zs;break;case"toggle":case"beforetoggle":x=xm}var V=(l&4)!==0,he=!V&&(e==="scroll"||e==="scrollend"),m=V?g!==null?g+"Capture":null:g;V=[];for(var o=v,p;o!==null;){var _=o;if(p=_.stateNode,_=_.tag,_!==5&&_!==26&&_!==27||p===null||m===null||(_=Ut(o,m),_!=null&&V.push(dn(o,_,p))),he)break;o=o.return}0<V.length&&(g=new x(g,Y,null,a,S),z.push({event:g,listeners:V}))}}if((l&7)===0){e:{if(g=e==="mouseover"||e==="pointerover",x=e==="mouseout"||e==="pointerout",g&&a!==tc&&(Y=a.relatedTarget||a.fromElement)&&(Za(Y)||Y[La]))break e;if((x||g)&&(g=S.window===S?S:(g=S.ownerDocument)?g.defaultView||g.parentWindow:window,x?(Y=a.relatedTarget||a.toElement,x=v,Y=Y?Za(Y):null,Y!==null&&(he=H(Y),V=Y.tag,Y!==he||V!==5&&V!==27&&V!==6)&&(Y=null)):(x=null,Y=v),x!==Y)){if(V=Qs,_="onMouseLeave",m="onMouseEnter",o="mouse",(e==="pointerout"||e==="pointerover")&&(V=Zs,_="onPointerLeave",m="onPointerEnter",o="pointer"),he=x==null?g:Mt(x),p=Y==null?g:Mt(Y),g=new V(_,o+"leave",x,a,S),g.target=he,g.relatedTarget=p,_=null,Za(S)===v&&(V=new V(m,o+"enter",Y,a,S),V.target=p,V.relatedTarget=he,_=V),he=_,x&&Y)l:{for(V=bh,m=x,o=Y,p=0,_=m;_;_=V(_))p++;_=0;for(var Z=o;Z;Z=V(Z))_++;for(;0<p-_;)m=V(m),p--;for(;0<_-p;)o=V(o),_--;for(;p--;){if(m===o||o!==null&&m===o.alternate){V=m;break l}m=V(m),o=V(o)}V=null}else V=null;x!==null&&Bo(z,g,x,V,!1),Y!==null&&he!==null&&Bo(z,he,Y,V,!0)}}e:{if(g=v?Mt(v):window,x=g.nodeName&&g.nodeName.toLowerCase(),x==="select"||x==="input"&&g.type==="file")var ne=Fs;else if($s(g))if(Ps)ne=Dm;else{ne=Am;var Q=Em}else x=g.nodeName,!x||x.toLowerCase()!=="input"||g.type!=="checkbox"&&g.type!=="radio"?v&&ac(v.elementType)&&(ne=Fs):ne=Om;if(ne&&(ne=ne(e,v))){Ws(z,ne,a,S);break e}Q&&Q(e,g,v),e==="focusout"&&v&&g.type==="number"&&v.memoizedProps.value!=null&&lc(g,"number",g.value)}switch(Q=v?Mt(v):window,e){case"focusin":($s(Q)||Q.contentEditable==="true")&&(Pa=Q,vc=v,Xt=null);break;case"focusout":Xt=vc=Pa=null;break;case"mousedown":gc=!0;break;case"contextmenu":case"mouseup":case"dragend":gc=!1,cr(z,a,S);break;case"selectionchange":if(Um)break;case"keydown":case"keyup":cr(z,a,S)}var F;if(dc)e:{switch(e){case"compositionstart":var ae="onCompositionStart";break e;case"compositionend":ae="onCompositionEnd";break e;case"compositionupdate":ae="onCompositionUpdate";break e}ae=void 0}else Fa?Ks(e,a)&&(ae="onCompositionEnd"):e==="keydown"&&a.keyCode===229&&(ae="onCompositionStart");ae&&(ws&&a.locale!=="ko"&&(Fa||ae!=="onCompositionStart"?ae==="onCompositionEnd"&&Fa&&(F=Gs()):(ea=S,uc="value"in ea?ea.value:ea.textContent,Fa=!0)),Q=zi(v,ae),0<Q.length&&(ae=new Ls(ae,e,null,a,S),z.push({event:ae,listeners:Q}),F?ae.data=F:(F=Js(a),F!==null&&(ae.data=F)))),(F=Sm?Nm(e,a):_m(e,a))&&(ae=zi(v,"onBeforeInput"),0<ae.length&&(Q=new Ls("onBeforeInput","beforeinput",null,a,S),z.push({event:Q,listeners:ae}),Q.data=F)),ph(z,e,v,a,S)}Ro(z,l)})}function dn(e,l,a){return{instance:e,listener:l,currentTarget:a}}function zi(e,l){for(var a=l+"Capture",t=[];e!==null;){var n=e,i=n.stateNode;if(n=n.tag,n!==5&&n!==26&&n!==27||i===null||(n=Ut(e,a),n!=null&&t.unshift(dn(e,n,i)),n=Ut(e,l),n!=null&&t.push(dn(e,n,i))),e.tag===3)return t;e=e.return}return[]}function bh(e){if(e===null)return null;do e=e.return;while(e&&e.tag!==5&&e.tag!==27);return e||null}function Bo(e,l,a,t,n){for(var i=l._reactName,u=[];a!==null&&a!==t;){var s=a,f=s.alternate,v=s.stateNode;if(s=s.tag,f!==null&&f===t)break;s!==5&&s!==26&&s!==27||v===null||(f=v,n?(v=Ut(a,i),v!=null&&u.unshift(dn(a,v,f))):n||(v=Ut(a,i),v!=null&&u.push(dn(a,v,f)))),a=a.return}u.length!==0&&e.push({event:l,listeners:u})}var xh=/\r\n?/g,jh=/\u0000|\uFFFD/g;function qo(e){return(typeof e=="string"?e:""+e).replace(xh,`
`).replace(jh,"")}function Yo(e,l){return l=qo(l),qo(e)===l}function me(e,l,a,t,n,i){switch(a){case"children":typeof t=="string"?l==="body"||l==="textarea"&&t===""||Ja(e,t):(typeof t=="number"||typeof t=="bigint")&&l!=="body"&&Ja(e,""+t);break;case"className":On(e,"class",t);break;case"tabIndex":On(e,"tabindex",t);break;case"dir":case"role":case"viewBox":case"width":case"height":On(e,a,t);break;case"style":Bs(e,t,i);break;case"data":if(l!=="object"){On(e,"data",t);break}case"src":case"href":if(t===""&&(l!=="a"||a!=="href")){e.removeAttribute(a);break}if(t==null||typeof t=="function"||typeof t=="symbol"||typeof t=="boolean"){e.removeAttribute(a);break}t=Mn(""+t),e.setAttribute(a,t);break;case"action":case"formAction":if(typeof t=="function"){e.setAttribute(a,"javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')");break}else typeof i=="function"&&(a==="formAction"?(l!=="input"&&me(e,l,"name",n.name,n,null),me(e,l,"formEncType",n.formEncType,n,null),me(e,l,"formMethod",n.formMethod,n,null),me(e,l,"formTarget",n.formTarget,n,null)):(me(e,l,"encType",n.encType,n,null),me(e,l,"method",n.method,n,null),me(e,l,"target",n.target,n,null)));if(t==null||typeof t=="symbol"||typeof t=="boolean"){e.removeAttribute(a);break}t=Mn(""+t),e.setAttribute(a,t);break;case"onClick":t!=null&&(e.onclick=Hl);break;case"onScroll":t!=null&&ee("scroll",e);break;case"onScrollEnd":t!=null&&ee("scrollend",e);break;case"dangerouslySetInnerHTML":if(t!=null){if(typeof t!="object"||!("__html"in t))throw Error(r(61));if(a=t.__html,a!=null){if(n.children!=null)throw Error(r(60));e.innerHTML=a}}break;case"multiple":e.multiple=t&&typeof t!="function"&&typeof t!="symbol";break;case"muted":e.muted=t&&typeof t!="function"&&typeof t!="symbol";break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"defaultValue":case"defaultChecked":case"innerHTML":case"ref":break;case"autoFocus":break;case"xlinkHref":if(t==null||typeof t=="function"||typeof t=="boolean"||typeof t=="symbol"){e.removeAttribute("xlink:href");break}a=Mn(""+t),e.setAttributeNS("http://www.w3.org/1999/xlink","xlink:href",a);break;case"contentEditable":case"spellCheck":case"draggable":case"value":case"autoReverse":case"externalResourcesRequired":case"focusable":case"preserveAlpha":t!=null&&typeof t!="function"&&typeof t!="symbol"?e.setAttribute(a,""+t):e.removeAttribute(a);break;case"inert":case"allowFullScreen":case"async":case"autoPlay":case"controls":case"default":case"defer":case"disabled":case"disablePictureInPicture":case"disableRemotePlayback":case"formNoValidate":case"hidden":case"loop":case"noModule":case"noValidate":case"open":case"playsInline":case"readOnly":case"required":case"reversed":case"scoped":case"seamless":case"itemScope":t&&typeof t!="function"&&typeof t!="symbol"?e.setAttribute(a,""):e.removeAttribute(a);break;case"capture":case"download":t===!0?e.setAttribute(a,""):t!==!1&&t!=null&&typeof t!="function"&&typeof t!="symbol"?e.setAttribute(a,t):e.removeAttribute(a);break;case"cols":case"rows":case"size":case"span":t!=null&&typeof t!="function"&&typeof t!="symbol"&&!isNaN(t)&&1<=t?e.setAttribute(a,t):e.removeAttribute(a);break;case"rowSpan":case"start":t==null||typeof t=="function"||typeof t=="symbol"||isNaN(t)?e.removeAttribute(a):e.setAttribute(a,t);break;case"popover":ee("beforetoggle",e),ee("toggle",e),An(e,"popover",t);break;case"xlinkActuate":Rl(e,"http://www.w3.org/1999/xlink","xlink:actuate",t);break;case"xlinkArcrole":Rl(e,"http://www.w3.org/1999/xlink","xlink:arcrole",t);break;case"xlinkRole":Rl(e,"http://www.w3.org/1999/xlink","xlink:role",t);break;case"xlinkShow":Rl(e,"http://www.w3.org/1999/xlink","xlink:show",t);break;case"xlinkTitle":Rl(e,"http://www.w3.org/1999/xlink","xlink:title",t);break;case"xlinkType":Rl(e,"http://www.w3.org/1999/xlink","xlink:type",t);break;case"xmlBase":Rl(e,"http://www.w3.org/XML/1998/namespace","xml:base",t);break;case"xmlLang":Rl(e,"http://www.w3.org/XML/1998/namespace","xml:lang",t);break;case"xmlSpace":Rl(e,"http://www.w3.org/XML/1998/namespace","xml:space",t);break;case"is":An(e,"is",t);break;case"innerText":case"textContent":break;default:(!(2<a.length)||a[0]!=="o"&&a[0]!=="O"||a[1]!=="n"&&a[1]!=="N")&&(a=$d.get(a)||a,An(e,a,t))}}function Lu(e,l,a,t,n,i){switch(a){case"style":Bs(e,t,i);break;case"dangerouslySetInnerHTML":if(t!=null){if(typeof t!="object"||!("__html"in t))throw Error(r(61));if(a=t.__html,a!=null){if(n.children!=null)throw Error(r(60));e.innerHTML=a}}break;case"children":typeof t=="string"?Ja(e,t):(typeof t=="number"||typeof t=="bigint")&&Ja(e,""+t);break;case"onScroll":t!=null&&ee("scroll",e);break;case"onScrollEnd":t!=null&&ee("scrollend",e);break;case"onClick":t!=null&&(e.onclick=Hl);break;case"suppressContentEditableWarning":case"suppressHydrationWarning":case"innerHTML":case"ref":break;case"innerText":case"textContent":break;default:if(!Es.hasOwnProperty(a))e:{if(a[0]==="o"&&a[1]==="n"&&(n=a.endsWith("Capture"),l=a.slice(2,n?a.length-7:void 0),i=e[We]||null,i=i!=null?i[a]:null,typeof i=="function"&&e.removeEventListener(l,i,n),typeof t=="function")){typeof i!="function"&&i!==null&&(a in e?e[a]=null:e.hasAttribute(a)&&e.removeAttribute(a)),e.addEventListener(l,t,n);break e}a in e?e[a]=t:t===!0?e.setAttribute(a,""):An(e,a,t)}}}function Ze(e,l,a){switch(l){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"img":ee("error",e),ee("load",e);var t=!1,n=!1,i;for(i in a)if(a.hasOwnProperty(i)){var u=a[i];if(u!=null)switch(i){case"src":t=!0;break;case"srcSet":n=!0;break;case"children":case"dangerouslySetInnerHTML":throw Error(r(137,l));default:me(e,l,i,u,a,null)}}n&&me(e,l,"srcSet",a.srcSet,a,null),t&&me(e,l,"src",a.src,a,null);return;case"input":ee("invalid",e);var s=i=u=n=null,f=null,v=null;for(t in a)if(a.hasOwnProperty(t)){var S=a[t];if(S!=null)switch(t){case"name":n=S;break;case"type":u=S;break;case"checked":f=S;break;case"defaultChecked":v=S;break;case"value":i=S;break;case"defaultValue":s=S;break;case"children":case"dangerouslySetInnerHTML":if(S!=null)throw Error(r(137,l));break;default:me(e,l,t,S,a,null)}}Us(e,i,s,f,v,u,n,!1);return;case"select":ee("invalid",e),t=u=i=null;for(n in a)if(a.hasOwnProperty(n)&&(s=a[n],s!=null))switch(n){case"value":i=s;break;case"defaultValue":u=s;break;case"multiple":t=s;default:me(e,l,n,s,a,null)}l=i,a=u,e.multiple=!!t,l!=null?Ka(e,!!t,l,!1):a!=null&&Ka(e,!!t,a,!0);return;case"textarea":ee("invalid",e),i=n=t=null;for(u in a)if(a.hasOwnProperty(u)&&(s=a[u],s!=null))switch(u){case"value":t=s;break;case"defaultValue":n=s;break;case"children":i=s;break;case"dangerouslySetInnerHTML":if(s!=null)throw Error(r(91));break;default:me(e,l,u,s,a,null)}Rs(e,t,n,i);return;case"option":for(f in a)a.hasOwnProperty(f)&&(t=a[f],t!=null)&&(f==="selected"?e.selected=t&&typeof t!="function"&&typeof t!="symbol":me(e,l,f,t,a,null));return;case"dialog":ee("beforetoggle",e),ee("toggle",e),ee("cancel",e),ee("close",e);break;case"iframe":case"object":ee("load",e);break;case"video":case"audio":for(t=0;t<on.length;t++)ee(on[t],e);break;case"image":ee("error",e),ee("load",e);break;case"details":ee("toggle",e);break;case"embed":case"source":case"link":ee("error",e),ee("load",e);case"area":case"base":case"br":case"col":case"hr":case"keygen":case"meta":case"param":case"track":case"wbr":case"menuitem":for(v in a)if(a.hasOwnProperty(v)&&(t=a[v],t!=null))switch(v){case"children":case"dangerouslySetInnerHTML":throw Error(r(137,l));default:me(e,l,v,t,a,null)}return;default:if(ac(l)){for(S in a)a.hasOwnProperty(S)&&(t=a[S],t!==void 0&&Lu(e,l,S,t,a,void 0));return}}for(s in a)a.hasOwnProperty(s)&&(t=a[s],t!=null&&me(e,l,s,t,a,null))}function Sh(e,l,a,t){switch(l){case"div":case"span":case"svg":case"path":case"a":case"g":case"p":case"li":break;case"input":var n=null,i=null,u=null,s=null,f=null,v=null,S=null;for(x in a){var z=a[x];if(a.hasOwnProperty(x)&&z!=null)switch(x){case"checked":break;case"value":break;case"defaultValue":f=z;default:t.hasOwnProperty(x)||me(e,l,x,null,t,z)}}for(var g in t){var x=t[g];if(z=a[g],t.hasOwnProperty(g)&&(x!=null||z!=null))switch(g){case"type":i=x;break;case"name":n=x;break;case"checked":v=x;break;case"defaultChecked":S=x;break;case"value":u=x;break;case"defaultValue":s=x;break;case"children":case"dangerouslySetInnerHTML":if(x!=null)throw Error(r(137,l));break;default:x!==z&&me(e,l,g,x,t,z)}}ec(e,u,s,f,v,S,i,n);return;case"select":x=u=s=g=null;for(i in a)if(f=a[i],a.hasOwnProperty(i)&&f!=null)switch(i){case"value":break;case"multiple":x=f;default:t.hasOwnProperty(i)||me(e,l,i,null,t,f)}for(n in t)if(i=t[n],f=a[n],t.hasOwnProperty(n)&&(i!=null||f!=null))switch(n){case"value":g=i;break;case"defaultValue":s=i;break;case"multiple":u=i;default:i!==f&&me(e,l,n,i,t,f)}l=s,a=u,t=x,g!=null?Ka(e,!!a,g,!1):!!t!=!!a&&(l!=null?Ka(e,!!a,l,!0):Ka(e,!!a,a?[]:"",!1));return;case"textarea":x=g=null;for(s in a)if(n=a[s],a.hasOwnProperty(s)&&n!=null&&!t.hasOwnProperty(s))switch(s){case"value":break;case"children":break;default:me(e,l,s,null,t,n)}for(u in t)if(n=t[u],i=a[u],t.hasOwnProperty(u)&&(n!=null||i!=null))switch(u){case"value":g=n;break;case"defaultValue":x=n;break;case"children":break;case"dangerouslySetInnerHTML":if(n!=null)throw Error(r(91));break;default:n!==i&&me(e,l,u,n,t,i)}Cs(e,g,x);return;case"option":for(var Y in a)g=a[Y],a.hasOwnProperty(Y)&&g!=null&&!t.hasOwnProperty(Y)&&(Y==="selected"?e.selected=!1:me(e,l,Y,null,t,g));for(f in t)g=t[f],x=a[f],t.hasOwnProperty(f)&&g!==x&&(g!=null||x!=null)&&(f==="selected"?e.selected=g&&typeof g!="function"&&typeof g!="symbol":me(e,l,f,g,t,x));return;case"img":case"link":case"area":case"base":case"br":case"col":case"embed":case"hr":case"keygen":case"meta":case"param":case"source":case"track":case"wbr":case"menuitem":for(var V in a)g=a[V],a.hasOwnProperty(V)&&g!=null&&!t.hasOwnProperty(V)&&me(e,l,V,null,t,g);for(v in t)if(g=t[v],x=a[v],t.hasOwnProperty(v)&&g!==x&&(g!=null||x!=null))switch(v){case"children":case"dangerouslySetInnerHTML":if(g!=null)throw Error(r(137,l));break;default:me(e,l,v,g,t,x)}return;default:if(ac(l)){for(var he in a)g=a[he],a.hasOwnProperty(he)&&g!==void 0&&!t.hasOwnProperty(he)&&Lu(e,l,he,void 0,t,g);for(S in t)g=t[S],x=a[S],!t.hasOwnProperty(S)||g===x||g===void 0&&x===void 0||Lu(e,l,S,g,t,x);return}}for(var m in a)g=a[m],a.hasOwnProperty(m)&&g!=null&&!t.hasOwnProperty(m)&&me(e,l,m,null,t,g);for(z in t)g=t[z],x=a[z],!t.hasOwnProperty(z)||g===x||g==null&&x==null||me(e,l,z,g,t,x)}function Go(e){switch(e){case"css":case"script":case"font":case"img":case"image":case"input":case"link":return!0;default:return!1}}function Nh(){if(typeof performance.getEntriesByType=="function"){for(var e=0,l=0,a=performance.getEntriesByType("resource"),t=0;t<a.length;t++){var n=a[t],i=n.transferSize,u=n.initiatorType,s=n.duration;if(i&&s&&Go(u)){for(u=0,s=n.responseEnd,t+=1;t<a.length;t++){var f=a[t],v=f.startTime;if(v>s)break;var S=f.transferSize,z=f.initiatorType;S&&Go(z)&&(f=f.responseEnd,u+=S*(f<s?1:(s-v)/(f-v)))}if(--t,l+=8*(i+u)/(n.duration/1e3),e++,10<e)break}}if(0<e)return l/e/1e6}return navigator.connection&&(e=navigator.connection.downlink,typeof e=="number")?e:5}var Zu=null,wu=null;function Ti(e){return e.nodeType===9?e:e.ownerDocument}function Xo(e){switch(e){case"http://www.w3.org/2000/svg":return 1;case"http://www.w3.org/1998/Math/MathML":return 2;default:return 0}}function Qo(e,l){if(e===0)switch(l){case"svg":return 1;case"math":return 2;default:return 0}return e===1&&l==="foreignObject"?0:e}function Vu(e,l){return e==="textarea"||e==="noscript"||typeof l.children=="string"||typeof l.children=="number"||typeof l.children=="bigint"||typeof l.dangerouslySetInnerHTML=="object"&&l.dangerouslySetInnerHTML!==null&&l.dangerouslySetInnerHTML.__html!=null}var ku=null;function _h(){var e=window.event;return e&&e.type==="popstate"?e===ku?!1:(ku=e,!0):(ku=null,!1)}var Lo=typeof setTimeout=="function"?setTimeout:void 0,zh=typeof clearTimeout=="function"?clearTimeout:void 0,Zo=typeof Promise=="function"?Promise:void 0,Th=typeof queueMicrotask=="function"?queueMicrotask:typeof Zo<"u"?function(e){return Zo.resolve(null).then(e).catch(Eh)}:Lo;function Eh(e){setTimeout(function(){throw e})}function ga(e){return e==="head"}function wo(e,l){var a=l,t=0;do{var n=a.nextSibling;if(e.removeChild(a),n&&n.nodeType===8)if(a=n.data,a==="/$"||a==="/&"){if(t===0){e.removeChild(n),zt(l);return}t--}else if(a==="$"||a==="$?"||a==="$~"||a==="$!"||a==="&")t++;else if(a==="html")mn(e.ownerDocument.documentElement);else if(a==="head"){a=e.ownerDocument.head,mn(a);for(var i=a.firstChild;i;){var u=i.nextSibling,s=i.nodeName;i[Dt]||s==="SCRIPT"||s==="STYLE"||s==="LINK"&&i.rel.toLowerCase()==="stylesheet"||a.removeChild(i),i=u}}else a==="body"&&mn(e.ownerDocument.body);a=n}while(a);zt(l)}function Vo(e,l){var a=e;e=0;do{var t=a.nextSibling;if(a.nodeType===1?l?(a._stashedDisplay=a.style.display,a.style.display="none"):(a.style.display=a._stashedDisplay||"",a.getAttribute("style")===""&&a.removeAttribute("style")):a.nodeType===3&&(l?(a._stashedText=a.nodeValue,a.nodeValue=""):a.nodeValue=a._stashedText||""),t&&t.nodeType===8)if(a=t.data,a==="/$"){if(e===0)break;e--}else a!=="$"&&a!=="$?"&&a!=="$~"&&a!=="$!"||e++;a=t}while(a)}function Ku(e){var l=e.firstChild;for(l&&l.nodeType===10&&(l=l.nextSibling);l;){var a=l;switch(l=l.nextSibling,a.nodeName){case"HTML":case"HEAD":case"BODY":Ku(a),Pi(a);continue;case"SCRIPT":case"STYLE":continue;case"LINK":if(a.rel.toLowerCase()==="stylesheet")continue}e.removeChild(a)}}function Ah(e,l,a,t){for(;e.nodeType===1;){var n=a;if(e.nodeName.toLowerCase()!==l.toLowerCase()){if(!t&&(e.nodeName!=="INPUT"||e.type!=="hidden"))break}else if(t){if(!e[Dt])switch(l){case"meta":if(!e.hasAttribute("itemprop"))break;return e;case"link":if(i=e.getAttribute("rel"),i==="stylesheet"&&e.hasAttribute("data-precedence"))break;if(i!==n.rel||e.getAttribute("href")!==(n.href==null||n.href===""?null:n.href)||e.getAttribute("crossorigin")!==(n.crossOrigin==null?null:n.crossOrigin)||e.getAttribute("title")!==(n.title==null?null:n.title))break;return e;case"style":if(e.hasAttribute("data-precedence"))break;return e;case"script":if(i=e.getAttribute("src"),(i!==(n.src==null?null:n.src)||e.getAttribute("type")!==(n.type==null?null:n.type)||e.getAttribute("crossorigin")!==(n.crossOrigin==null?null:n.crossOrigin))&&i&&e.hasAttribute("async")&&!e.hasAttribute("itemprop"))break;return e;default:return e}}else if(l==="input"&&e.type==="hidden"){var i=n.name==null?null:""+n.name;if(n.type==="hidden"&&e.getAttribute("name")===i)return e}else return e;if(e=_l(e.nextSibling),e===null)break}return null}function Oh(e,l,a){if(l==="")return null;for(;e.nodeType!==3;)if((e.nodeType!==1||e.nodeName!=="INPUT"||e.type!=="hidden")&&!a||(e=_l(e.nextSibling),e===null))return null;return e}function ko(e,l){for(;e.nodeType!==8;)if((e.nodeType!==1||e.nodeName!=="INPUT"||e.type!=="hidden")&&!l||(e=_l(e.nextSibling),e===null))return null;return e}function Ju(e){return e.data==="$?"||e.data==="$~"}function $u(e){return e.data==="$!"||e.data==="$?"&&e.ownerDocument.readyState!=="loading"}function Dh(e,l){var a=e.ownerDocument;if(e.data==="$~")e._reactRetry=l;else if(e.data!=="$?"||a.readyState!=="loading")l();else{var t=function(){l(),a.removeEventListener("DOMContentLoaded",t)};a.addEventListener("DOMContentLoaded",t),e._reactRetry=t}}function _l(e){for(;e!=null;e=e.nextSibling){var l=e.nodeType;if(l===1||l===3)break;if(l===8){if(l=e.data,l==="$"||l==="$!"||l==="$?"||l==="$~"||l==="&"||l==="F!"||l==="F")break;if(l==="/$"||l==="/&")return null}}return e}var Wu=null;function Ko(e){e=e.nextSibling;for(var l=0;e;){if(e.nodeType===8){var a=e.data;if(a==="/$"||a==="/&"){if(l===0)return _l(e.nextSibling);l--}else a!=="$"&&a!=="$!"&&a!=="$?"&&a!=="$~"&&a!=="&"||l++}e=e.nextSibling}return null}function Jo(e){e=e.previousSibling;for(var l=0;e;){if(e.nodeType===8){var a=e.data;if(a==="$"||a==="$!"||a==="$?"||a==="$~"||a==="&"){if(l===0)return e;l--}else a!=="/$"&&a!=="/&"||l++}e=e.previousSibling}return null}function $o(e,l,a){switch(l=Ti(a),e){case"html":if(e=l.documentElement,!e)throw Error(r(452));return e;case"head":if(e=l.head,!e)throw Error(r(453));return e;case"body":if(e=l.body,!e)throw Error(r(454));return e;default:throw Error(r(451))}}function mn(e){for(var l=e.attributes;l.length;)e.removeAttributeNode(l[0]);Pi(e)}var zl=new Map,Wo=new Set;function Ei(e){return typeof e.getRootNode=="function"?e.getRootNode():e.nodeType===9?e:e.ownerDocument}var Fl=R.d;R.d={f:Mh,r:Uh,D:Ch,C:Rh,L:Hh,m:Bh,X:Yh,S:qh,M:Gh};function Mh(){var e=Fl.f(),l=yi();return e||l}function Uh(e){var l=wa(e);l!==null&&l.tag===5&&l.type==="form"?df(l):Fl.r(e)}var St=typeof document>"u"?null:document;function Fo(e,l,a){var t=St;if(t&&typeof l=="string"&&l){var n=gl(l);n='link[rel="'+e+'"][href="'+n+'"]',typeof a=="string"&&(n+='[crossorigin="'+a+'"]'),Wo.has(n)||(Wo.add(n),e={rel:e,crossOrigin:a,href:l},t.querySelector(n)===null&&(l=t.createElement("link"),Ze(l,"link",e),He(l),t.head.appendChild(l)))}}function Ch(e){Fl.D(e),Fo("dns-prefetch",e,null)}function Rh(e,l){Fl.C(e,l),Fo("preconnect",e,l)}function Hh(e,l,a){Fl.L(e,l,a);var t=St;if(t&&e&&l){var n='link[rel="preload"][as="'+gl(l)+'"]';l==="image"&&a&&a.imageSrcSet?(n+='[imagesrcset="'+gl(a.imageSrcSet)+'"]',typeof a.imageSizes=="string"&&(n+='[imagesizes="'+gl(a.imageSizes)+'"]')):n+='[href="'+gl(e)+'"]';var i=n;switch(l){case"style":i=Nt(e);break;case"script":i=_t(e)}zl.has(i)||(e=A({rel:"preload",href:l==="image"&&a&&a.imageSrcSet?void 0:e,as:l},a),zl.set(i,e),t.querySelector(n)!==null||l==="style"&&t.querySelector(hn(i))||l==="script"&&t.querySelector(pn(i))||(l=t.createElement("link"),Ze(l,"link",e),He(l),t.head.appendChild(l)))}}function Bh(e,l){Fl.m(e,l);var a=St;if(a&&e){var t=l&&typeof l.as=="string"?l.as:"script",n='link[rel="modulepreload"][as="'+gl(t)+'"][href="'+gl(e)+'"]',i=n;switch(t){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":i=_t(e)}if(!zl.has(i)&&(e=A({rel:"modulepreload",href:e},l),zl.set(i,e),a.querySelector(n)===null)){switch(t){case"audioworklet":case"paintworklet":case"serviceworker":case"sharedworker":case"worker":case"script":if(a.querySelector(pn(i)))return}t=a.createElement("link"),Ze(t,"link",e),He(t),a.head.appendChild(t)}}}function qh(e,l,a){Fl.S(e,l,a);var t=St;if(t&&e){var n=Va(t).hoistableStyles,i=Nt(e);l=l||"default";var u=n.get(i);if(!u){var s={loading:0,preload:null};if(u=t.querySelector(hn(i)))s.loading=5;else{e=A({rel:"stylesheet",href:e,"data-precedence":l},a),(a=zl.get(i))&&Fu(e,a);var f=u=t.createElement("link");He(f),Ze(f,"link",e),f._p=new Promise(function(v,S){f.onload=v,f.onerror=S}),f.addEventListener("load",function(){s.loading|=1}),f.addEventListener("error",function(){s.loading|=2}),s.loading|=4,Ai(u,l,t)}u={type:"stylesheet",instance:u,count:1,state:s},n.set(i,u)}}}function Yh(e,l){Fl.X(e,l);var a=St;if(a&&e){var t=Va(a).hoistableScripts,n=_t(e),i=t.get(n);i||(i=a.querySelector(pn(n)),i||(e=A({src:e,async:!0},l),(l=zl.get(n))&&Pu(e,l),i=a.createElement("script"),He(i),Ze(i,"link",e),a.head.appendChild(i)),i={type:"script",instance:i,count:1,state:null},t.set(n,i))}}function Gh(e,l){Fl.M(e,l);var a=St;if(a&&e){var t=Va(a).hoistableScripts,n=_t(e),i=t.get(n);i||(i=a.querySelector(pn(n)),i||(e=A({src:e,async:!0,type:"module"},l),(l=zl.get(n))&&Pu(e,l),i=a.createElement("script"),He(i),Ze(i,"link",e),a.head.appendChild(i)),i={type:"script",instance:i,count:1,state:null},t.set(n,i))}}function Po(e,l,a,t){var n=(n=X.current)?Ei(n):null;if(!n)throw Error(r(446));switch(e){case"meta":case"title":return null;case"style":return typeof a.precedence=="string"&&typeof a.href=="string"?(l=Nt(a.href),a=Va(n).hoistableStyles,t=a.get(l),t||(t={type:"style",instance:null,count:0,state:null},a.set(l,t)),t):{type:"void",instance:null,count:0,state:null};case"link":if(a.rel==="stylesheet"&&typeof a.href=="string"&&typeof a.precedence=="string"){e=Nt(a.href);var i=Va(n).hoistableStyles,u=i.get(e);if(u||(n=n.ownerDocument||n,u={type:"stylesheet",instance:null,count:0,state:{loading:0,preload:null}},i.set(e,u),(i=n.querySelector(hn(e)))&&!i._p&&(u.instance=i,u.state.loading=5),zl.has(e)||(a={rel:"preload",as:"style",href:a.href,crossOrigin:a.crossOrigin,integrity:a.integrity,media:a.media,hrefLang:a.hrefLang,referrerPolicy:a.referrerPolicy},zl.set(e,a),i||Xh(n,e,a,u.state))),l&&t===null)throw Error(r(528,""));return u}if(l&&t!==null)throw Error(r(529,""));return null;case"script":return l=a.async,a=a.src,typeof a=="string"&&l&&typeof l!="function"&&typeof l!="symbol"?(l=_t(a),a=Va(n).hoistableScripts,t=a.get(l),t||(t={type:"script",instance:null,count:0,state:null},a.set(l,t)),t):{type:"void",instance:null,count:0,state:null};default:throw Error(r(444,e))}}function Nt(e){return'href="'+gl(e)+'"'}function hn(e){return'link[rel="stylesheet"]['+e+"]"}function Io(e){return A({},e,{"data-precedence":e.precedence,precedence:null})}function Xh(e,l,a,t){e.querySelector('link[rel="preload"][as="style"]['+l+"]")?t.loading=1:(l=e.createElement("link"),t.preload=l,l.addEventListener("load",function(){return t.loading|=1}),l.addEventListener("error",function(){return t.loading|=2}),Ze(l,"link",a),He(l),e.head.appendChild(l))}function _t(e){return'[src="'+gl(e)+'"]'}function pn(e){return"script[async]"+e}function ed(e,l,a){if(l.count++,l.instance===null)switch(l.type){case"style":var t=e.querySelector('style[data-href~="'+gl(a.href)+'"]');if(t)return l.instance=t,He(t),t;var n=A({},a,{"data-href":a.href,"data-precedence":a.precedence,href:null,precedence:null});return t=(e.ownerDocument||e).createElement("style"),He(t),Ze(t,"style",n),Ai(t,a.precedence,e),l.instance=t;case"stylesheet":n=Nt(a.href);var i=e.querySelector(hn(n));if(i)return l.state.loading|=4,l.instance=i,He(i),i;t=Io(a),(n=zl.get(n))&&Fu(t,n),i=(e.ownerDocument||e).createElement("link"),He(i);var u=i;return u._p=new Promise(function(s,f){u.onload=s,u.onerror=f}),Ze(i,"link",t),l.state.loading|=4,Ai(i,a.precedence,e),l.instance=i;case"script":return i=_t(a.src),(n=e.querySelector(pn(i)))?(l.instance=n,He(n),n):(t=a,(n=zl.get(i))&&(t=A({},a),Pu(t,n)),e=e.ownerDocument||e,n=e.createElement("script"),He(n),Ze(n,"link",t),e.head.appendChild(n),l.instance=n);case"void":return null;default:throw Error(r(443,l.type))}else l.type==="stylesheet"&&(l.state.loading&4)===0&&(t=l.instance,l.state.loading|=4,Ai(t,a.precedence,e));return l.instance}function Ai(e,l,a){for(var t=a.querySelectorAll('link[rel="stylesheet"][data-precedence],style[data-precedence]'),n=t.length?t[t.length-1]:null,i=n,u=0;u<t.length;u++){var s=t[u];if(s.dataset.precedence===l)i=s;else if(i!==n)break}i?i.parentNode.insertBefore(e,i.nextSibling):(l=a.nodeType===9?a.head:a,l.insertBefore(e,l.firstChild))}function Fu(e,l){e.crossOrigin==null&&(e.crossOrigin=l.crossOrigin),e.referrerPolicy==null&&(e.referrerPolicy=l.referrerPolicy),e.title==null&&(e.title=l.title)}function Pu(e,l){e.crossOrigin==null&&(e.crossOrigin=l.crossOrigin),e.referrerPolicy==null&&(e.referrerPolicy=l.referrerPolicy),e.integrity==null&&(e.integrity=l.integrity)}var Oi=null;function ld(e,l,a){if(Oi===null){var t=new Map,n=Oi=new Map;n.set(a,t)}else n=Oi,t=n.get(a),t||(t=new Map,n.set(a,t));if(t.has(e))return t;for(t.set(e,null),a=a.getElementsByTagName(e),n=0;n<a.length;n++){var i=a[n];if(!(i[Dt]||i[Ge]||e==="link"&&i.getAttribute("rel")==="stylesheet")&&i.namespaceURI!=="http://www.w3.org/2000/svg"){var u=i.getAttribute(l)||"";u=e+u;var s=t.get(u);s?s.push(i):t.set(u,[i])}}return t}function ad(e,l,a){e=e.ownerDocument||e,e.head.insertBefore(a,l==="title"?e.querySelector("head > title"):null)}function Qh(e,l,a){if(a===1||l.itemProp!=null)return!1;switch(e){case"meta":case"title":return!0;case"style":if(typeof l.precedence!="string"||typeof l.href!="string"||l.href==="")break;return!0;case"link":if(typeof l.rel!="string"||typeof l.href!="string"||l.href===""||l.onLoad||l.onError)break;return l.rel==="stylesheet"?(e=l.disabled,typeof l.precedence=="string"&&e==null):!0;case"script":if(l.async&&typeof l.async!="function"&&typeof l.async!="symbol"&&!l.onLoad&&!l.onError&&l.src&&typeof l.src=="string")return!0}return!1}function td(e){return!(e.type==="stylesheet"&&(e.state.loading&3)===0)}function Lh(e,l,a,t){if(a.type==="stylesheet"&&(typeof t.media!="string"||matchMedia(t.media).matches!==!1)&&(a.state.loading&4)===0){if(a.instance===null){var n=Nt(t.href),i=l.querySelector(hn(n));if(i){l=i._p,l!==null&&typeof l=="object"&&typeof l.then=="function"&&(e.count++,e=Di.bind(e),l.then(e,e)),a.state.loading|=4,a.instance=i,He(i);return}i=l.ownerDocument||l,t=Io(t),(n=zl.get(n))&&Fu(t,n),i=i.createElement("link"),He(i);var u=i;u._p=new Promise(function(s,f){u.onload=s,u.onerror=f}),Ze(i,"link",t),a.instance=i}e.stylesheets===null&&(e.stylesheets=new Map),e.stylesheets.set(a,l),(l=a.state.preload)&&(a.state.loading&3)===0&&(e.count++,a=Di.bind(e),l.addEventListener("load",a),l.addEventListener("error",a))}}var Iu=0;function Zh(e,l){return e.stylesheets&&e.count===0&&Ui(e,e.stylesheets),0<e.count||0<e.imgCount?function(a){var t=setTimeout(function(){if(e.stylesheets&&Ui(e,e.stylesheets),e.unsuspend){var i=e.unsuspend;e.unsuspend=null,i()}},6e4+l);0<e.imgBytes&&Iu===0&&(Iu=62500*Nh());var n=setTimeout(function(){if(e.waitingForImages=!1,e.count===0&&(e.stylesheets&&Ui(e,e.stylesheets),e.unsuspend)){var i=e.unsuspend;e.unsuspend=null,i()}},(e.imgBytes>Iu?50:800)+l);return e.unsuspend=a,function(){e.unsuspend=null,clearTimeout(t),clearTimeout(n)}}:null}function Di(){if(this.count--,this.count===0&&(this.imgCount===0||!this.waitingForImages)){if(this.stylesheets)Ui(this,this.stylesheets);else if(this.unsuspend){var e=this.unsuspend;this.unsuspend=null,e()}}}var Mi=null;function Ui(e,l){e.stylesheets=null,e.unsuspend!==null&&(e.count++,Mi=new Map,l.forEach(wh,e),Mi=null,Di.call(e))}function wh(e,l){if(!(l.state.loading&4)){var a=Mi.get(e);if(a)var t=a.get(null);else{a=new Map,Mi.set(e,a);for(var n=e.querySelectorAll("link[data-precedence],style[data-precedence]"),i=0;i<n.length;i++){var u=n[i];(u.nodeName==="LINK"||u.getAttribute("media")!=="not all")&&(a.set(u.dataset.precedence,u),t=u)}t&&a.set(null,t)}n=l.instance,u=n.getAttribute("data-precedence"),i=a.get(u)||t,i===t&&a.set(null,n),a.set(u,n),this.count++,t=Di.bind(this),n.addEventListener("load",t),n.addEventListener("error",t),i?i.parentNode.insertBefore(n,i.nextSibling):(e=e.nodeType===9?e.head:e,e.insertBefore(n,e.firstChild)),l.state.loading|=4}}var vn={$$typeof:ve,Provider:null,Consumer:null,_currentValue:k,_currentValue2:k,_threadCount:0};function Vh(e,l,a,t,n,i,u,s,f){this.tag=1,this.containerInfo=e,this.pingCache=this.current=this.pendingChildren=null,this.timeoutHandle=-1,this.callbackNode=this.next=this.pendingContext=this.context=this.cancelPendingCommit=null,this.callbackPriority=0,this.expirationTimes=Ji(-1),this.entangledLanes=this.shellSuspendCounter=this.errorRecoveryDisabledLanes=this.expiredLanes=this.warmLanes=this.pingedLanes=this.suspendedLanes=this.pendingLanes=0,this.entanglements=Ji(0),this.hiddenUpdates=Ji(null),this.identifierPrefix=t,this.onUncaughtError=n,this.onCaughtError=i,this.onRecoverableError=u,this.pooledCache=null,this.pooledCacheLanes=0,this.formState=f,this.incompleteTransitions=new Map}function nd(e,l,a,t,n,i,u,s,f,v,S,z){return e=new Vh(e,l,a,u,f,v,S,z,s),l=1,i===!0&&(l|=24),i=fl(3,null,null,l),e.current=i,i.stateNode=e,l=Uc(),l.refCount++,e.pooledCache=l,l.refCount++,i.memoizedState={element:t,isDehydrated:a,cache:l},Bc(i),e}function id(e){return e?(e=lt,e):lt}function cd(e,l,a,t,n,i){n=id(n),t.context===null?t.context=n:t.pendingContext=n,t=ca(l),t.payload={element:a},i=i===void 0?null:i,i!==null&&(t.callback=i),a=ua(e,t,l),a!==null&&(al(a,e,l),Kt(a,e,l))}function ud(e,l){if(e=e.memoizedState,e!==null&&e.dehydrated!==null){var a=e.retryLane;e.retryLane=a!==0&&a<l?a:l}}function es(e,l){ud(e,l),(e=e.alternate)&&ud(e,l)}function sd(e){if(e.tag===13||e.tag===31){var l=Oa(e,67108864);l!==null&&al(l,e,67108864),es(e,67108864)}}function rd(e){if(e.tag===13||e.tag===31){var l=pl();l=$i(l);var a=Oa(e,l);a!==null&&al(a,e,l),es(e,l)}}var Ci=!0;function kh(e,l,a,t){var n=N.T;N.T=null;var i=R.p;try{R.p=2,ls(e,l,a,t)}finally{R.p=i,N.T=n}}function Kh(e,l,a,t){var n=N.T;N.T=null;var i=R.p;try{R.p=8,ls(e,l,a,t)}finally{R.p=i,N.T=n}}function ls(e,l,a,t){if(Ci){var n=as(t);if(n===null)Qu(e,l,t,Ri,a),od(e,t);else if($h(n,e,l,a,t))t.stopPropagation();else if(od(e,t),l&4&&-1<Jh.indexOf(e)){for(;n!==null;){var i=wa(n);if(i!==null)switch(i.tag){case 3:if(i=i.stateNode,i.current.memoizedState.isDehydrated){var u=_a(i.pendingLanes);if(u!==0){var s=i;for(s.pendingLanes|=2,s.entangledLanes|=2;u;){var f=1<<31-sl(u);s.entanglements[1]|=f,u&=~f}Cl(i),(ce&6)===0&&(vi=cl()+500,fn(0))}}break;case 31:case 13:s=Oa(i,2),s!==null&&al(s,i,2),yi(),es(i,2)}if(i=as(t),i===null&&Qu(e,l,t,Ri,a),i===n)break;n=i}n!==null&&t.stopPropagation()}else Qu(e,l,t,null,a)}}function as(e){return e=nc(e),ts(e)}var Ri=null;function ts(e){if(Ri=null,e=Za(e),e!==null){var l=H(e);if(l===null)e=null;else{var a=l.tag;if(a===13){if(e=B(l),e!==null)return e;e=null}else if(a===31){if(e=D(l),e!==null)return e;e=null}else if(a===3){if(l.stateNode.current.memoizedState.isDehydrated)return l.tag===3?l.stateNode.containerInfo:null;e=null}else l!==e&&(e=null)}}return Ri=e,null}function fd(e){switch(e){case"beforetoggle":case"cancel":case"click":case"close":case"contextmenu":case"copy":case"cut":case"auxclick":case"dblclick":case"dragend":case"dragstart":case"drop":case"focusin":case"focusout":case"input":case"invalid":case"keydown":case"keypress":case"keyup":case"mousedown":case"mouseup":case"paste":case"pause":case"play":case"pointercancel":case"pointerdown":case"pointerup":case"ratechange":case"reset":case"resize":case"seeked":case"submit":case"toggle":case"touchcancel":case"touchend":case"touchstart":case"volumechange":case"change":case"selectionchange":case"textInput":case"compositionstart":case"compositionend":case"compositionupdate":case"beforeblur":case"afterblur":case"beforeinput":case"blur":case"fullscreenchange":case"focus":case"hashchange":case"popstate":case"select":case"selectstart":return 2;case"drag":case"dragenter":case"dragexit":case"dragleave":case"dragover":case"mousemove":case"mouseout":case"mouseover":case"pointermove":case"pointerout":case"pointerover":case"scroll":case"touchmove":case"wheel":case"mouseenter":case"mouseleave":case"pointerenter":case"pointerleave":return 8;case"message":switch(Cd()){case vs:return 2;case gs:return 8;case Nn:case Rd:return 32;case ys:return 268435456;default:return 32}default:return 32}}var ns=!1,ya=null,ba=null,xa=null,gn=new Map,yn=new Map,ja=[],Jh="mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(" ");function od(e,l){switch(e){case"focusin":case"focusout":ya=null;break;case"dragenter":case"dragleave":ba=null;break;case"mouseover":case"mouseout":xa=null;break;case"pointerover":case"pointerout":gn.delete(l.pointerId);break;case"gotpointercapture":case"lostpointercapture":yn.delete(l.pointerId)}}function bn(e,l,a,t,n,i){return e===null||e.nativeEvent!==i?(e={blockedOn:l,domEventName:a,eventSystemFlags:t,nativeEvent:i,targetContainers:[n]},l!==null&&(l=wa(l),l!==null&&sd(l)),e):(e.eventSystemFlags|=t,l=e.targetContainers,n!==null&&l.indexOf(n)===-1&&l.push(n),e)}function $h(e,l,a,t,n){switch(l){case"focusin":return ya=bn(ya,e,l,a,t,n),!0;case"dragenter":return ba=bn(ba,e,l,a,t,n),!0;case"mouseover":return xa=bn(xa,e,l,a,t,n),!0;case"pointerover":var i=n.pointerId;return gn.set(i,bn(gn.get(i)||null,e,l,a,t,n)),!0;case"gotpointercapture":return i=n.pointerId,yn.set(i,bn(yn.get(i)||null,e,l,a,t,n)),!0}return!1}function dd(e){var l=Za(e.target);if(l!==null){var a=H(l);if(a!==null){if(l=a.tag,l===13){if(l=B(a),l!==null){e.blockedOn=l,_s(e.priority,function(){rd(a)});return}}else if(l===31){if(l=D(a),l!==null){e.blockedOn=l,_s(e.priority,function(){rd(a)});return}}else if(l===3&&a.stateNode.current.memoizedState.isDehydrated){e.blockedOn=a.tag===3?a.stateNode.containerInfo:null;return}}}e.blockedOn=null}function Hi(e){if(e.blockedOn!==null)return!1;for(var l=e.targetContainers;0<l.length;){var a=as(e.nativeEvent);if(a===null){a=e.nativeEvent;var t=new a.constructor(a.type,a);tc=t,a.target.dispatchEvent(t),tc=null}else return l=wa(a),l!==null&&sd(l),e.blockedOn=a,!1;l.shift()}return!0}function md(e,l,a){Hi(e)&&a.delete(l)}function Wh(){ns=!1,ya!==null&&Hi(ya)&&(ya=null),ba!==null&&Hi(ba)&&(ba=null),xa!==null&&Hi(xa)&&(xa=null),gn.forEach(md),yn.forEach(md)}function Bi(e,l){e.blockedOn===l&&(e.blockedOn=null,ns||(ns=!0,j.unstable_scheduleCallback(j.unstable_NormalPriority,Wh)))}var qi=null;function hd(e){qi!==e&&(qi=e,j.unstable_scheduleCallback(j.unstable_NormalPriority,function(){qi===e&&(qi=null);for(var l=0;l<e.length;l+=3){var a=e[l],t=e[l+1],n=e[l+2];if(typeof t!="function"){if(ts(t||a)===null)continue;break}var i=wa(a);i!==null&&(e.splice(l,3),l-=3,au(i,{pending:!0,data:n,method:a.method,action:t},t,n))}}))}function zt(e){function l(f){return Bi(f,e)}ya!==null&&Bi(ya,e),ba!==null&&Bi(ba,e),xa!==null&&Bi(xa,e),gn.forEach(l),yn.forEach(l);for(var a=0;a<ja.length;a++){var t=ja[a];t.blockedOn===e&&(t.blockedOn=null)}for(;0<ja.length&&(a=ja[0],a.blockedOn===null);)dd(a),a.blockedOn===null&&ja.shift();if(a=(e.ownerDocument||e).$$reactFormReplay,a!=null)for(t=0;t<a.length;t+=3){var n=a[t],i=a[t+1],u=n[We]||null;if(typeof i=="function")u||hd(a);else if(u){var s=null;if(i&&i.hasAttribute("formAction")){if(n=i,u=i[We]||null)s=u.formAction;else if(ts(n)!==null)continue}else s=u.action;typeof s=="function"?a[t+1]=s:(a.splice(t,3),t-=3),hd(a)}}}function pd(){function e(i){i.canIntercept&&i.info==="react-transition"&&i.intercept({handler:function(){return new Promise(function(u){return n=u})},focusReset:"manual",scroll:"manual"})}function l(){n!==null&&(n(),n=null),t||setTimeout(a,20)}function a(){if(!t&&!navigation.transition){var i=navigation.currentEntry;i&&i.url!=null&&navigation.navigate(i.url,{state:i.getState(),info:"react-transition",history:"replace"})}}if(typeof navigation=="object"){var t=!1,n=null;return navigation.addEventListener("navigate",e),navigation.addEventListener("navigatesuccess",l),navigation.addEventListener("navigateerror",l),setTimeout(a,100),function(){t=!0,navigation.removeEventListener("navigate",e),navigation.removeEventListener("navigatesuccess",l),navigation.removeEventListener("navigateerror",l),n!==null&&(n(),n=null)}}}function is(e){this._internalRoot=e}Yi.prototype.render=is.prototype.render=function(e){var l=this._internalRoot;if(l===null)throw Error(r(409));var a=l.current,t=pl();cd(a,t,e,l,null,null)},Yi.prototype.unmount=is.prototype.unmount=function(){var e=this._internalRoot;if(e!==null){this._internalRoot=null;var l=e.containerInfo;cd(e.current,2,null,e,null,null),yi(),l[La]=null}};function Yi(e){this._internalRoot=e}Yi.prototype.unstable_scheduleHydration=function(e){if(e){var l=Ns();e={blockedOn:null,target:e,priority:l};for(var a=0;a<ja.length&&l!==0&&l<ja[a].priority;a++);ja.splice(a,0,e),a===0&&dd(e)}};var vd=w.version;if(vd!=="19.2.4")throw Error(r(527,vd,"19.2.4"));R.findDOMNode=function(e){var l=e._reactInternals;if(l===void 0)throw typeof e.render=="function"?Error(r(188)):(e=Object.keys(e).join(","),Error(r(268,e)));return e=h(l),e=e!==null?O(e):null,e=e===null?null:e.stateNode,e};var Fh={bundleType:0,version:"19.2.4",rendererPackageName:"react-dom",currentDispatcherRef:N,reconcilerVersion:"19.2.4"};if(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__<"u"){var Gi=__REACT_DEVTOOLS_GLOBAL_HOOK__;if(!Gi.isDisabled&&Gi.supportsFiber)try{Et=Gi.inject(Fh),ul=Gi}catch{}}return jn.createRoot=function(e,l){if(!b(e))throw Error(r(299));var a=!1,t="",n=Sf,i=Nf,u=_f;return l!=null&&(l.unstable_strictMode===!0&&(a=!0),l.identifierPrefix!==void 0&&(t=l.identifierPrefix),l.onUncaughtError!==void 0&&(n=l.onUncaughtError),l.onCaughtError!==void 0&&(i=l.onCaughtError),l.onRecoverableError!==void 0&&(u=l.onRecoverableError)),l=nd(e,1,!1,null,null,a,t,null,n,i,u,pd),e[La]=l.current,Xu(e),new is(l)},jn.hydrateRoot=function(e,l,a){if(!b(e))throw Error(r(299));var t=!1,n="",i=Sf,u=Nf,s=_f,f=null;return a!=null&&(a.unstable_strictMode===!0&&(t=!0),a.identifierPrefix!==void 0&&(n=a.identifierPrefix),a.onUncaughtError!==void 0&&(i=a.onUncaughtError),a.onCaughtError!==void 0&&(u=a.onCaughtError),a.onRecoverableError!==void 0&&(s=a.onRecoverableError),a.formState!==void 0&&(f=a.formState)),l=nd(e,1,!0,l,a??null,t,n,f,i,u,s,pd),l.context=id(null),a=l.current,t=pl(),t=$i(t),n=ca(t),n.callback=null,ua(a,n,t),a=t,l.current.lanes=a,Ot(l,a),Cl(l),e[La]=l.current,Xu(e),new Yi(l)},jn.version="19.2.4",jn}var Td;function up(){if(Td)return ss.exports;Td=1;function j(){if(!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__>"u"||typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE!="function"))try{__REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(j)}catch(w){console.error(w)}}return j(),ss.exports=cp(),ss.exports}var sp=up();function rp({onOpenTalent:j}){const[w,L]=G.useState([]),[r,b]=G.useState(""),[H,B]=G.useState(""),[D,E]=G.useState(!0);G.useEffect(()=>{const O=new URLSearchParams;r&&O.set("search",r),H&&O.set("domain",H),fetch(`/api/roster?${O}`).then(A=>A.json()).then(A=>{L(A.roster),E(!1)}).catch(()=>E(!1))},[r,H]);const h=[...new Set(w.flatMap(O=>O.domains_of_practice))];return D?c.jsx("div",{className:"loading",children:"Loading roster..."}):c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"Talent Roster"}),c.jsx("p",{children:"Every person profiled by their practice, body of work, and what they bring to a production table."})]}),c.jsxs("div",{className:"search-bar",children:[c.jsx("input",{className:"search-input",type:"text",placeholder:"Search by name, practice, domain, or keyword...",value:r,onChange:O=>b(O.target.value)}),c.jsx("button",{className:`filter-btn ${H===""?"active":""}`,onClick:()=>B(""),children:"All"}),h.slice(0,6).map(O=>c.jsx("button",{className:`filter-btn ${H===O?"active":""}`,onClick:()=>B(H===O?"":O),children:O.split(" ").slice(0,2).join(" ")},O))]}),c.jsx("div",{className:"grid-2",children:w.map(O=>c.jsxs("div",{className:"card card-clickable talent-card",onClick:()=>j(O.talent_id),children:[c.jsxs("div",{className:"talent-card-header",children:[c.jsxs("div",{children:[c.jsx("div",{className:"talent-name",children:O.name}),c.jsx("div",{className:"talent-practice",children:O.domains_of_practice.slice(0,2).join(" / ")})]}),c.jsx("span",{className:`tag ${O.availability==="available"?"available":"on-production"}`,children:O.availability==="available"?"Available":O.availability.replace("_"," ")})]}),c.jsxs("p",{className:"talent-bio",children:[O.bio.slice(0,180),"..."]}),c.jsxs("div",{className:"talent-card-footer",children:[c.jsx("div",{className:"tags",children:O.resonance_tags.slice(0,5).map(A=>c.jsx("span",{className:"tag",children:A},A))}),c.jsxs("div",{className:"talent-scores",children:[O.total_cosm>0&&c.jsxs("span",{className:"score-value cosm",children:[O.total_cosm.toFixed(0)," Cosm"]}),O.total_chron>0&&c.jsxs("span",{className:"score-value chron",children:[O.total_chron.toFixed(0)," Chron"]}),O.productions_completed.length>0&&c.jsxs("span",{className:"talent-prod-count",children:[O.productions_completed.length," prod."]})]})]})]},O.talent_id))}),w.length===0&&c.jsxs("div",{className:"empty-state",children:[c.jsx("h3",{children:"No practitioners found"}),c.jsx("p",{children:"Try adjusting your search or filters."})]}),c.jsx("style",{children:`
        .talent-card-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 0.75rem;
        }
        .talent-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.15rem;
          font-weight: 600;
          margin-bottom: 0.15rem;
        }
        .talent-practice {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.04em;
        }
        .talent-bio {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
          margin-bottom: 0.75rem;
        }
        .talent-card-footer {
          display: flex;
          justify-content: space-between;
          align-items: flex-end;
          gap: 0.5rem;
        }
        .talent-scores {
          display: flex;
          gap: 0.5rem;
          align-items: center;
          font-size: 0.8rem;
          flex-shrink: 0;
        }
        .talent-prod-count {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          font-weight: 500;
        }
      `})]})}function fp({onOpenPrincipal:j}){const[w,L]=G.useState([]),[r,b]=G.useState(""),[H,B]=G.useState(!0);return G.useEffect(()=>{const D=r?`?game_type=${r}`:"";fetch(`/api/principals${D}`).then(E=>E.json()).then(E=>{L(E.principals),B(!1)}).catch(()=>B(!1))},[r]),H?c.jsx("div",{className:"loading",children:"Loading principals..."}):c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"Production Principals"}),c.jsx("p",{children:"Top-tier production leaders whose vision shapes how a dome gets designed or a sphere comes alive. The principal's name goes on the production."})]}),c.jsxs("div",{className:"search-bar",children:[c.jsx("button",{className:`filter-btn ${r===""?"active":""}`,onClick:()=>b(""),children:"All"}),c.jsx("button",{className:`filter-btn ${r==="domes"?"active":""}`,onClick:()=>b("domes"),children:"Domes"}),c.jsx("button",{className:`filter-btn ${r==="spheres"?"active":""}`,onClick:()=>b("spheres"),children:"Spheres"})]}),c.jsx("div",{className:"principals-grid",children:w.map(D=>c.jsxs("div",{className:"card card-clickable principal-card",onClick:()=>j(D.principal_id),children:[c.jsxs("div",{className:"principal-header",children:[c.jsxs("div",{className:"principal-name-row",children:[c.jsx("h3",{className:"principal-name",children:D.name}),D.game_type&&c.jsx("span",{className:`badge badge-${D.game_type}`,children:D.game_type.toUpperCase()})]}),c.jsx("p",{className:"principal-bio",children:D.bio})]}),c.jsxs("div",{className:"principal-vision",children:[c.jsx("div",{className:"vision-label",children:"VISION"}),c.jsxs("p",{children:[D.vision.slice(0,200),"..."]})]}),c.jsx("div",{className:"principal-works",children:D.body_of_work.slice(0,3).map((E,h)=>c.jsxs("div",{className:"principal-work-pill",children:[c.jsx("span",{className:"pw-title",children:E.title}),E.year&&c.jsx("span",{className:"pw-year",children:E.year})]},h))}),D.signature_style&&c.jsx("div",{className:"principal-signature",children:c.jsxs("em",{children:['"',D.signature_style.slice(0,120),'"']})}),c.jsxs("div",{className:"principal-footer",children:[c.jsxs("span",{className:"principal-prods",children:[D.productions_led.length," productions"]}),D.total_cosm>0&&c.jsxs("span",{className:"score-value cosm",children:[D.total_cosm.toFixed(0)," Cosm"]}),D.total_chron>0&&c.jsxs("span",{className:"score-value chron",children:[D.total_chron.toFixed(0)," Chron"]})]})]},D.principal_id))}),c.jsx("style",{children:`
        .principals-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(420px, 1fr));
          gap: 1.25rem;
        }
        .principal-card {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .principal-name-row {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 0.5rem;
        }
        .principal-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.3rem;
          font-weight: 600;
        }
        .principal-bio {
          font-size: 0.95rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .principal-vision {
          padding: 1rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
        }
        .vision-label {
          font-size: 0.7rem;
          font-weight: 600;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          color: var(--accent-dark);
          margin-bottom: 0.35rem;
        }
        .principal-vision p {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
          font-style: italic;
        }
        .principal-works {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .principal-work-pill {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.3rem 0.65rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: 20px;
          font-size: 0.8rem;
        }
        .pw-title {
          font-weight: 500;
          color: var(--ink-light);
        }
        .pw-year {
          color: var(--ink-lighter);
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.7rem;
        }
        .principal-signature {
          font-size: 0.85rem;
          color: var(--ink-lighter);
          padding-left: 0.75rem;
          border-left: 2px solid var(--accent-light);
        }
        .principal-footer {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding-top: 0.5rem;
          border-top: 1px solid var(--border-light);
        }
        .principal-prods {
          font-size: 0.8rem;
          color: var(--ink-lighter);
          font-weight: 500;
        }
      `})]})}const Ed={development:"Development",pre_production:"Pre-Production",production:"Production",post_production:"Post-Production",distribution:"Distribution"},Ad=["development","pre_production","production","post_production","distribution"];function op({onOpenProject:j}){const[w,L]=G.useState([]),[r,b]=G.useState(""),[H,B]=G.useState(""),[D,E]=G.useState(!0);G.useEffect(()=>{const U=new URLSearchParams;r&&U.set("game_type",r),H&&U.set("status",H),fetch(`/api/projects?${U}`).then(se=>se.json()).then(se=>{L(se.projects),E(!1)}).catch(()=>E(!1))},[r,H]);const h=w.filter(U=>U.status==="in_production"),O=w.filter(U=>U.status==="sourced"),A=w.filter(U=>U.status==="assembling"),W=w.filter(U=>["completed","published"].includes(U.status));return D?c.jsx("div",{className:"loading",children:"Loading projects..."}):c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"Project Board"}),c.jsx("p",{children:"All productions — sourced, assembling, in production, and completed."})]}),c.jsxs("div",{className:"search-bar",children:[c.jsx("button",{className:`filter-btn ${r===""?"active":""}`,onClick:()=>b(""),children:"All"}),c.jsx("button",{className:`filter-btn ${r==="domes"?"active":""}`,onClick:()=>b("domes"),children:"Domes"}),c.jsx("button",{className:`filter-btn ${r==="spheres"?"active":""}`,onClick:()=>b("spheres"),children:"Spheres"}),c.jsx("div",{style:{width:1,background:"var(--border)",margin:"0 0.25rem"}}),c.jsx("button",{className:`filter-btn ${H===""?"active":""}`,onClick:()=>B(""),children:"All Status"}),c.jsx("button",{className:`filter-btn ${H==="sourced"?"active":""}`,onClick:()=>B("sourced"),children:"Sourced"}),c.jsx("button",{className:`filter-btn ${H==="in_production"?"active":""}`,onClick:()=>B("in_production"),children:"Active"}),c.jsx("button",{className:`filter-btn ${H==="completed"?"active":""}`,onClick:()=>B("completed"),children:"Done"})]}),h.length>0&&c.jsxs("div",{className:"board-section",children:[c.jsx("h3",{className:"board-section-title",children:"In Production"}),c.jsx("div",{className:"grid-2",children:h.map(U=>c.jsx(Xi,{project:U,onClick:()=>j(U.project_id)},U.project_id))})]}),A.length>0&&c.jsxs("div",{className:"board-section",children:[c.jsx("h3",{className:"board-section-title",children:"Assembling Teams"}),c.jsx("div",{className:"grid-2",children:A.map(U=>c.jsx(Xi,{project:U,onClick:()=>j(U.project_id)},U.project_id))})]}),O.length>0&&c.jsxs("div",{className:"board-section",children:[c.jsx("h3",{className:"board-section-title",children:"Sourced — Ready for Teams"}),c.jsx("div",{className:"grid-2",children:O.map(U=>c.jsx(Xi,{project:U,onClick:()=>j(U.project_id)},U.project_id))})]}),W.length>0&&c.jsxs("div",{className:"board-section",children:[c.jsx("h3",{className:"board-section-title",children:"Completed"}),c.jsx("div",{className:"grid-2",children:W.map(U=>c.jsx(Xi,{project:U,onClick:()=>j(U.project_id)},U.project_id))})]}),c.jsx("style",{children:`
        .board-section {
          margin-bottom: 2.5rem;
        }
        .board-section-title {
          font-family: 'Inter', sans-serif;
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
          margin-bottom: 1rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid var(--border-light);
        }
      `})]})}function Xi({project:j,onClick:w}){const r=j.game_type==="domes"?j.character?.name:j.parcel?.address,b=j.current_stage?Ad.indexOf(j.current_stage):-1,H=b>=0?(b+1)/5*100:0;return c.jsxs("div",{className:"card card-clickable project-card",onClick:w,children:[c.jsxs("div",{className:"project-card-top",children:[c.jsxs("div",{children:[c.jsx("div",{className:"project-title",children:j.title}),r&&c.jsx("div",{className:"project-subject",children:r})]}),c.jsxs("div",{className:"project-badges",children:[c.jsx("span",{className:`badge badge-${j.game_type}`,children:j.game_type.toUpperCase()}),c.jsx("span",{className:`badge badge-status ${j.status}`,children:j.status.replace("_"," ")})]})]}),j.current_stage&&c.jsxs("div",{className:"project-stage",children:[c.jsxs("div",{className:"stage-track",children:[Ad.map((B,D)=>c.jsx("div",{className:`stage-dot ${D<=b?"filled":""} ${j.current_stage===B?"current":""}`,title:Ed[B]},B)),c.jsx("div",{className:"stage-line",children:c.jsx("div",{className:"stage-line-fill",style:{width:`${H}%`}})})]}),c.jsx("span",{className:"stage-label",children:Ed[j.current_stage]})]}),j.team_ids?.length>0&&c.jsxs("div",{className:"project-team-count",children:[j.team_ids.length," team members"]}),c.jsxs("div",{className:"project-scores",children:[j.cosm_score>0&&c.jsxs("span",{className:"score-value cosm",children:[j.cosm_score.toFixed(1)," Cosm"]}),j.chron_score>0&&c.jsxs("span",{className:"score-value chron",children:[j.chron_score.toFixed(1)," Chron"]})]}),c.jsx("style",{children:`
        .project-card {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .project-card-top {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }
        .project-title {
          font-family: 'Playfair Display', serif;
          font-size: 1.1rem;
          font-weight: 600;
          margin-bottom: 0.15rem;
        }
        .project-subject {
          font-size: 0.85rem;
          color: var(--ink-lighter);
        }
        .project-badges {
          display: flex;
          gap: 0.35rem;
          flex-shrink: 0;
        }
        .project-stage {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        .stage-track {
          flex: 1;
          display: flex;
          align-items: center;
          gap: 0;
          position: relative;
          padding: 0 4px;
        }
        .stage-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--paper-dark);
          border: 1.5px solid var(--border);
          position: relative;
          z-index: 2;
          flex-shrink: 0;
        }
        .stage-dot.filled {
          background: var(--accent);
          border-color: var(--accent);
        }
        .stage-dot.current {
          background: var(--ink);
          border-color: var(--ink);
          box-shadow: 0 0 0 3px rgba(26,26,26,0.15);
        }
        .stage-dot + .stage-dot {
          margin-left: calc(25% - 8px);
        }
        .stage-line {
          position: absolute;
          left: 8px;
          right: 8px;
          height: 2px;
          background: var(--border-light);
          z-index: 1;
        }
        .stage-line-fill {
          height: 100%;
          background: var(--accent);
          transition: width 0.4s ease;
        }
        .stage-label {
          font-size: 0.75rem;
          font-weight: 500;
          color: var(--ink-lighter);
          white-space: nowrap;
        }
        .project-team-count {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .project-scores {
          display: flex;
          gap: 0.75rem;
        }
      `})]})}function dp({onOpenProject:j}){const[w,L]=G.useState([]),[r,b]=G.useState(""),[H,B]=G.useState(!0);if(G.useEffect(()=>{const h=new URLSearchParams;r&&h.set("game_type",r),h.set("status","sourced"),fetch(`/api/projects?${h}`).then(O=>O.json()).then(O=>{L(O.projects),B(!1)}).catch(()=>B(!1))},[r]),H)return c.jsx("div",{className:"loading",children:"Loading sourced projects..."});const D=w.filter(h=>h.game_type==="domes"),E=w.filter(h=>h.game_type==="spheres");return c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"Project Sourcing"}),c.jsx("p",{children:"Characters sourced from documented material for domes. Parcels sourced from real data for spheres. Each brief describes the production challenge."})]}),c.jsxs("div",{className:"search-bar",children:[c.jsx("button",{className:`filter-btn ${r===""?"active":""}`,onClick:()=>b(""),children:"All"}),c.jsx("button",{className:`filter-btn ${r==="domes"?"active":""}`,onClick:()=>b("domes"),children:"Domes Characters"}),c.jsx("button",{className:`filter-btn ${r==="spheres"?"active":""}`,onClick:()=>b("spheres"),children:"Spheres Parcels"})]}),(r===""||r==="domes")&&D.length>0&&c.jsxs("div",{className:"sourcing-section",children:[c.jsxs("div",{className:"sourcing-section-header",children:[c.jsx("span",{className:"badge badge-domes",children:"DOMES"}),c.jsx("h3",{children:"Character Briefs"}),c.jsx("p",{children:"Sourced from books, films, journalism, and case studies"})]}),c.jsx("div",{className:"sourcing-grid",children:D.map(h=>c.jsxs("div",{className:"card card-clickable source-card",onClick:()=>j(h.project_id),children:[c.jsxs("div",{className:"source-card-header",children:[c.jsx("h4",{className:"source-title",children:h.title}),c.jsx("span",{className:"badge badge-domes",children:"DOMES"})]}),h.character&&c.jsxs(c.Fragment,{children:[c.jsxs("div",{className:"source-meta",children:[c.jsx("span",{className:"source-name",children:h.character.name}),c.jsxs("span",{className:"source-from",children:["from ",c.jsx("em",{children:h.character.source})]})]}),c.jsxs("p",{className:"source-situation",children:[h.character.situation.slice(0,180),"..."]}),c.jsxs("div",{className:"source-challenge",children:[c.jsx("div",{className:"challenge-label",children:"Production Challenge"}),c.jsxs("p",{children:[h.character.production_challenge.slice(0,150),"..."]})]}),c.jsx("div",{className:"source-tags",children:h.character.key_systems.slice(0,4).map(O=>c.jsx("span",{className:"tag",children:O},O))}),c.jsx("div",{className:"source-flourishing",children:h.character.flourishing_dimensions.map(O=>c.jsx("span",{className:"flourishing-dim",children:O},O))})]})]},h.project_id))})]}),(r===""||r==="spheres")&&E.length>0&&c.jsxs("div",{className:"sourcing-section",children:[c.jsxs("div",{className:"sourcing-section-header",children:[c.jsx("span",{className:"badge badge-spheres",children:"SPHERES"}),c.jsx("h3",{children:"Parcel Briefs"}),c.jsx("p",{children:"Real parcels from Philadelphia with documented activation opportunities"})]}),c.jsx("div",{className:"sourcing-grid",children:E.map(h=>c.jsxs("div",{className:"card card-clickable source-card",onClick:()=>j(h.project_id),children:[c.jsxs("div",{className:"source-card-header",children:[c.jsx("h4",{className:"source-title",children:h.title}),c.jsx("span",{className:"badge badge-spheres",children:"SPHERES"})]}),h.parcel&&c.jsxs(c.Fragment,{children:[c.jsxs("div",{className:"parcel-meta",children:[c.jsx("div",{className:"parcel-address",children:h.parcel.address}),c.jsxs("div",{className:"parcel-details",children:[c.jsx("span",{children:h.parcel.neighborhood}),c.jsx("span",{className:"parcel-sep",children:"/"}),c.jsx("span",{children:h.parcel.zoning}),c.jsx("span",{className:"parcel-sep",children:"/"}),c.jsxs("span",{className:"mono",children:[h.parcel.lot_size_sqft.toLocaleString()," sqft"]})]})]}),c.jsxs("p",{className:"source-history",children:[h.parcel.history.slice(0,160),"..."]}),c.jsxs("div",{className:"source-challenge",children:[c.jsx("div",{className:"challenge-label",children:"Activation Opportunity"}),c.jsxs("p",{children:[h.parcel.opportunity.slice(0,150),"..."]})]}),c.jsx("div",{className:"source-tags",children:h.parcel.constraints.map((O,A)=>c.jsx("span",{className:"tag",children:O.slice(0,30)},A))})]})]},h.project_id))})]}),c.jsx("style",{children:`
        .sourcing-section {
          margin-bottom: 3rem;
        }
        .sourcing-section-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1.25rem;
          flex-wrap: wrap;
        }
        .sourcing-section-header h3 {
          font-family: 'Inter', sans-serif;
          font-size: 1rem;
          font-weight: 600;
        }
        .sourcing-section-header p {
          width: 100%;
          font-size: 0.85rem;
          color: var(--ink-lighter);
          margin-top: 0.25rem;
        }
        .sourcing-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
          gap: 1.25rem;
        }
        .source-card {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .source-card-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }
        .source-title {
          font-family: 'Playfair Display', serif;
          font-size: 1.1rem;
          font-weight: 600;
        }
        .source-meta {
          display: flex;
          flex-direction: column;
          gap: 0.15rem;
        }
        .source-name {
          font-weight: 600;
          font-size: 0.95rem;
        }
        .source-from {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .source-situation, .source-history {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .source-challenge {
          padding: 0.75rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
        }
        .challenge-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
          margin-bottom: 0.25rem;
        }
        .source-challenge p {
          font-size: 0.85rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .source-tags {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
        }
        .parcel-meta {
          display: flex;
          flex-direction: column;
          gap: 0.2rem;
        }
        .parcel-address {
          font-weight: 600;
          font-size: 0.95rem;
        }
        .parcel-details {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .parcel-sep {
          color: var(--border);
        }
        .source-flourishing {
          display: flex;
          flex-wrap: wrap;
          gap: 0.35rem;
        }
        .flourishing-dim {
          font-size: 0.7rem;
          padding: 0.15rem 0.45rem;
          background: var(--domes-bg);
          color: var(--domes-color);
          border-radius: 20px;
          font-weight: 500;
        }
      `})]})}function mp({onOpenProject:j,onOpenTalent:w}){const[L,r]=G.useState([]),[b,H]=G.useState([]),[B,D]=G.useState(null),[E,h]=G.useState(""),[O,A]=G.useState(null),[W,U]=G.useState(!1),[se,_e]=G.useState(!0);G.useEffect(()=>{Promise.all([fetch("/api/projects?status=sourced").then(q=>q.json()),fetch("/api/principals").then(q=>q.json())]).then(([q,be])=>{r(q.projects),H(be.principals),_e(!1)}).catch(()=>_e(!1))},[]);const tl=async()=>{if(!B)return;U(!0),A(null);const q=new URLSearchParams;E&&q.set("principal_id",E),q.set("team_size","6");try{const ve=await(await fetch(`/api/projects/${B.project_id}/assemble?${q}`,{method:"POST"})).json();A(ve)}catch(be){console.error("Assembly failed:",be)}U(!1)};return se?c.jsx("div",{className:"loading",children:"Loading..."}):c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"Team Assembly"}),c.jsx("p",{children:"Select a project, optionally choose a principal, and let the agent assemble a team based on resonance — not role-filling, but genuine matchmaking between practices and production challenge."})]}),c.jsxs("div",{className:"assembly-controls",children:[c.jsxs("div",{className:"assembly-step",children:[c.jsx("div",{className:"step-label",children:"1. Select Project"}),c.jsx("div",{className:"project-select-grid",children:L.map(q=>c.jsxs("div",{className:`project-select-card ${B?.project_id===q.project_id?"selected":""}`,onClick:()=>{D(q),A(null)},children:[c.jsx("span",{className:`badge badge-${q.game_type}`,children:q.game_type.toUpperCase()}),c.jsx("span",{className:"psc-title",children:q.title})]},q.project_id))})]}),B&&c.jsxs("div",{className:"assembly-step",children:[c.jsx("div",{className:"step-label",children:"2. Choose Principal (optional — agent will recommend)"}),c.jsxs("div",{className:"principal-select-grid",children:[c.jsxs("div",{className:`principal-select-card ${E===""?"selected":""}`,onClick:()=>h(""),children:[c.jsx("span",{className:"psc-name",children:"Agent's Choice"}),c.jsx("span",{className:"psc-desc",children:"Let the agent recommend a principal"})]}),b.filter(q=>!B.game_type||!q.game_type||q.game_type===B.game_type).map(q=>c.jsxs("div",{className:`principal-select-card ${E===q.principal_id?"selected":""}`,onClick:()=>h(q.principal_id),children:[c.jsx("span",{className:"psc-name",children:q.name}),c.jsxs("span",{className:"psc-desc",children:[q.signature_style?.slice(0,60)||q.bio.slice(0,60),"..."]})]},q.principal_id))]})]}),B&&c.jsx("button",{className:"btn btn-primary assemble-btn",onClick:tl,disabled:W,children:W?"Assembling...":"Assemble Team"})]}),O&&c.jsxs("div",{className:"team-result",children:[c.jsx("div",{className:"section-divider"}),c.jsx("h3",{className:"team-result-title",children:"Assembled Team"}),c.jsxs("div",{className:"team-principal-card",children:[c.jsx("div",{className:"tp-label",children:"PRINCIPAL"}),c.jsx("div",{className:"tp-name",children:O.principal_name})]}),c.jsxs("div",{className:"team-strength",children:[c.jsx("div",{className:"ts-label",children:"Team Strength"}),c.jsx("p",{children:O.team_strength})]}),O.unlikely_collisions?.length>0&&c.jsxs("div",{className:"team-unlikely",children:[c.jsx("div",{className:"ts-label",children:"Unlikely Collisions"}),O.unlikely_collisions.map((q,be)=>c.jsx("p",{className:"unlikely-item",children:q},be))]}),c.jsxs("div",{className:"team-capabilities",children:[c.jsx("div",{className:"ts-label",children:"Capabilities Coverage"}),c.jsx("div",{className:"caps-grid",children:Object.entries(O.capabilities_coverage||{}).map(([q,be])=>c.jsxs("div",{className:`cap-item ${be?"covered":"missing"}`,children:[c.jsx("span",{className:"cap-icon",children:be?"✓":"✗"}),c.jsx("span",{children:q.replace("_"," ")})]},q))})]}),O.ip_surface_area?.length>0&&c.jsxs("div",{className:"team-ip-surface",children:[c.jsx("div",{className:"ts-label",children:"Expected IP Surface Area"}),c.jsx("div",{className:"tags",children:O.ip_surface_area.map(q=>c.jsx("span",{className:"tag",children:q.replace("_"," ")},q))})]}),c.jsxs("div",{className:"team-members",children:[c.jsx("div",{className:"ts-label",children:"Team Members"}),O.members?.map((q,be)=>c.jsxs("div",{className:"team-member-card card",onClick:()=>w(q.talent_id),style:{cursor:"pointer"},children:[c.jsxs("div",{className:"tm-header",children:[c.jsx("span",{className:"tm-name",children:q.talent_name}),c.jsxs("span",{className:"tm-score",children:[q.resonance_score.toFixed(0)," resonance"]})]}),c.jsx("div",{className:"resonance-bar-container",children:c.jsx("div",{className:"resonance-bar",style:{width:`${q.resonance_score}%`}})}),c.jsx("p",{className:"tm-reasoning",children:q.reasoning}),q.unlikely_value&&c.jsx("div",{className:"tm-unlikely",children:q.unlikely_value}),q.capabilities_matched?.length>0&&c.jsx("div",{className:"tags",style:{marginTop:"0.35rem"},children:q.capabilities_matched.map(ve=>c.jsx("span",{className:"tag",children:ve.replace("_"," ")},ve))})]},q.talent_id))]})]}),c.jsx("style",{children:`
        .assembly-controls {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }
        .assembly-step {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .step-label {
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-lighter);
        }
        .project-select-grid, .principal-select-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .project-select-card, .principal-select-card {
          padding: 0.6rem 1rem;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          background: white;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          transition: all 0.2s;
        }
        .project-select-card:hover, .principal-select-card:hover {
          border-color: var(--accent);
        }
        .project-select-card.selected, .principal-select-card.selected {
          border-color: var(--ink);
          background: var(--ink);
          color: white;
        }
        .project-select-card.selected .badge { opacity: 0.7; }
        .psc-title, .psc-name {
          font-weight: 600;
          font-size: 0.9rem;
        }
        .psc-desc {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .principal-select-card.selected .psc-desc { color: rgba(255,255,255,0.7); }
        .assemble-btn {
          align-self: flex-start;
          padding: 0.75rem 2rem;
          font-size: 0.95rem;
        }
        .team-result {
          margin-top: 1rem;
        }
        .team-result-title {
          font-size: 1.3rem;
          margin-bottom: 1.25rem;
        }
        .team-principal-card {
          padding: 1.25rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-md);
          margin-bottom: 1.25rem;
        }
        .tp-label {
          font-size: 0.7rem;
          font-weight: 600;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          opacity: 0.6;
          margin-bottom: 0.25rem;
        }
        .tp-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.5rem;
          font-weight: 600;
        }
        .team-strength, .team-unlikely, .team-capabilities, .team-ip-surface {
          margin-bottom: 1.25rem;
        }
        .ts-label {
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-lighter);
          margin-bottom: 0.5rem;
        }
        .team-strength p, .team-unlikely p {
          font-size: 0.95rem;
          color: var(--ink-light);
          line-height: 1.6;
        }
        .unlikely-item {
          font-style: italic;
          padding-left: 0.75rem;
          border-left: 2px solid var(--accent-light);
          margin-bottom: 0.5rem;
        }
        .caps-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
        }
        .cap-item {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.35rem 0.75rem;
          border-radius: 20px;
          font-size: 0.8rem;
          font-weight: 500;
        }
        .cap-item.covered {
          background: var(--success-bg);
          color: var(--success);
        }
        .cap-item.missing {
          background: var(--spheres-bg);
          color: var(--spheres-color);
        }
        .team-members {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .team-member-card {
          padding: 1rem 1.25rem;
        }
        .tm-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.25rem;
        }
        .tm-name {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 1rem;
        }
        .tm-score {
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
        }
        .tm-reasoning {
          font-size: 0.85rem;
          color: var(--ink-light);
          line-height: 1.5;
          margin-top: 0.5rem;
        }
        .tm-unlikely {
          font-size: 0.8rem;
          font-style: italic;
          color: var(--accent-dark);
          margin-top: 0.35rem;
        }
      `})]})}function hp(){const[j,w]=G.useState([]),[L,r]=G.useState([]),[b,H]=G.useState(""),[B,D]=G.useState(""),[E,h]=G.useState({}),[O,A]=G.useState(!0);G.useEffect(()=>{fetch("/api/ip/domains").then(U=>U.json()).then(U=>r(U.domains)).catch(()=>{})},[]),G.useEffect(()=>{const U=new URLSearchParams;b&&U.set("domain",b),B&&U.set("search",B),fetch(`/api/ip?${U}`).then(se=>se.json()).then(se=>{w(se.ip_items),h(se.by_domain||{}),A(!1)}).catch(()=>A(!1))},[b,B]);const W=Object.values(E).reduce((U,se)=>U+se,0);return c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"IP Dashboard"}),c.jsx("p",{children:"Every innovation across all productions — categorized by domain, attributed to the practice that produced it."})]}),c.jsx("div",{className:"ip-domains-grid",children:L.map(U=>c.jsxs("div",{className:`ip-domain-card ${b===U.domain?"selected":""}`,onClick:()=>H(b===U.domain?"":U.domain),children:[c.jsx("div",{className:"ipd-count",children:U.count}),c.jsx("div",{className:"ipd-label",children:U.label})]},U.domain))}),c.jsxs("div",{className:"ip-summary",children:[c.jsxs("span",{className:"ip-total",children:[W," total IP items"]}),c.jsxs("span",{className:"ip-domains-count",children:[L.filter(U=>U.count>0).length," active domains"]})]}),c.jsxs("div",{className:"search-bar",children:[c.jsx("input",{className:"search-input",type:"text",placeholder:"Search IP by title, description, or practice...",value:B,onChange:U=>D(U.target.value)}),b&&c.jsxs("button",{className:"filter-btn active",onClick:()=>H(""),children:[b.replace("_"," ")," x"]})]}),j.length>0?c.jsx("div",{className:"ip-list",children:j.map(U=>c.jsxs("div",{className:"card ip-item-card",children:[c.jsxs("div",{className:"ip-item-header",children:[c.jsxs("div",{children:[c.jsx("div",{className:"ip-item-title",children:U.title}),c.jsxs("div",{className:"ip-item-meta",children:[c.jsx("span",{className:"tag",children:U.domain.replace("_"," ")}),c.jsx("span",{className:"ip-format",children:U.format})]})]}),c.jsxs("div",{className:"ip-item-production",children:[c.jsx("span",{className:"ip-prod-title",children:U.production_title}),c.jsx("span",{className:"ip-stage",children:U.stage_originated.replace("_"," ")})]})]}),c.jsx("p",{className:"ip-item-desc",children:U.description}),c.jsxs("div",{className:"ip-item-footer",children:[c.jsxs("span",{className:"ip-practitioner",children:[U.practitioner_name," ",c.jsxs("span",{className:"ip-practice",children:["(",U.practice,")"]})]}),c.jsx("span",{className:"ip-value",children:U.value_driver})]})]},U.ip_id))}):c.jsxs("div",{className:"empty-state",children:[c.jsx("h3",{children:O?"Loading...":"No IP items yet"}),c.jsx("p",{children:"IP is generated as productions move through the pipeline. Each team member's practice produces domain-specific innovations."})]}),c.jsx("style",{children:`
        .ip-domains-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }
        .ip-domain-card {
          padding: 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          text-align: center;
          cursor: pointer;
          transition: all 0.2s;
        }
        .ip-domain-card:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .ip-domain-card.selected {
          background: var(--ink);
          color: white;
          border-color: var(--ink);
        }
        .ipd-count {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.5rem;
          font-weight: 600;
          margin-bottom: 0.25rem;
        }
        .ip-domain-card.selected .ipd-count { color: var(--accent-light); }
        .ipd-label {
          font-size: 0.75rem;
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          color: var(--ink-lighter);
        }
        .ip-domain-card.selected .ipd-label { color: rgba(255,255,255,0.7); }
        .ip-summary {
          display: flex;
          gap: 1.5rem;
          margin-bottom: 1.25rem;
        }
        .ip-total {
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.9rem;
          font-weight: 500;
          color: var(--ink-light);
        }
        .ip-domains-count {
          font-size: 0.85rem;
          color: var(--ink-lighter);
        }
        .ip-list {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .ip-item-card {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .ip-item-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
        }
        .ip-item-title {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 1rem;
          margin-bottom: 0.25rem;
        }
        .ip-item-meta {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        .ip-format {
          font-size: 0.8rem;
          color: var(--ink-lighter);
          font-style: italic;
        }
        .ip-item-production {
          text-align: right;
          flex-shrink: 0;
        }
        .ip-prod-title {
          display: block;
          font-size: 0.8rem;
          font-weight: 500;
          color: var(--ink-light);
        }
        .ip-stage {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          text-transform: capitalize;
        }
        .ip-item-desc {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .ip-item-footer {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding-top: 0.5rem;
          border-top: 1px solid var(--border-light);
        }
        .ip-practitioner {
          font-size: 0.85rem;
          font-weight: 500;
        }
        .ip-practice {
          font-weight: 400;
          color: var(--ink-lighter);
          font-style: italic;
        }
        .ip-value {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
        }
      `})]})}function pp({onOpenTalent:j,onOpenPrincipal:w}){const[L,r]=G.useState([]),[b,H]=G.useState("flourishing"),[B,D]=G.useState(!0);return G.useEffect(()=>{fetch(`/api/leaderboard?sort_by=${b}`).then(E=>E.json()).then(E=>{r(E.leaderboard),D(!1)}).catch(()=>D(!1))},[b]),B?c.jsx("div",{className:"loading",children:"Loading leaderboard..."}):c.jsxs("div",{children:[c.jsxs("div",{className:"page-header",children:[c.jsx("h2",{children:"Leaderboard"}),c.jsx("p",{children:"Individual and team Cosm/Chron scores, IP output by domain, productions completed."})]}),c.jsxs("div",{className:"search-bar",children:[c.jsx("button",{className:`filter-btn ${b==="flourishing"?"active":""}`,onClick:()=>H("flourishing"),children:"Flourishing"}),c.jsx("button",{className:`filter-btn ${b==="cosm"?"active":""}`,onClick:()=>H("cosm"),children:"Cosm"}),c.jsx("button",{className:`filter-btn ${b==="chron"?"active":""}`,onClick:()=>H("chron"),children:"Chron"}),c.jsx("button",{className:`filter-btn ${b==="productions"?"active":""}`,onClick:()=>H("productions"),children:"Productions"}),c.jsx("button",{className:`filter-btn ${b==="ip"?"active":""}`,onClick:()=>H("ip"),children:"IP Output"})]}),c.jsxs("div",{className:"leaderboard-table",children:[c.jsxs("div",{className:"lb-header",children:[c.jsx("span",{className:"lb-rank",children:"#"}),c.jsx("span",{className:"lb-name-col",children:"Name"}),c.jsx("span",{className:"lb-role-col",children:"Role"}),c.jsx("span",{className:"lb-num-col",children:"Productions"}),c.jsx("span",{className:"lb-num-col",children:"Cosm"}),c.jsx("span",{className:"lb-num-col",children:"Chron"}),c.jsx("span",{className:"lb-num-col",children:"Flourishing"}),c.jsx("span",{className:"lb-num-col",children:"IP"})]}),L.map((E,h)=>c.jsxs("div",{className:"lb-row card-clickable",onClick:()=>E.role==="talent"?j(E.id):w(E.id),children:[c.jsx("span",{className:"lb-rank",children:h+1}),c.jsxs("span",{className:"lb-name-col",children:[c.jsx("span",{className:"lb-name",children:E.name}),E.domains_of_practice?.length>0&&c.jsx("span",{className:"lb-practice",children:E.domains_of_practice[0]})]}),c.jsx("span",{className:"lb-role-col",children:c.jsx("span",{className:`badge ${E.role==="principal"?"badge-principal":"badge-talent"}`,children:E.role})}),c.jsx("span",{className:"lb-num-col mono",children:E.productions_completed}),c.jsx("span",{className:"lb-num-col mono score-value cosm",children:E.total_cosm.toFixed(1)}),c.jsx("span",{className:"lb-num-col mono score-value chron",children:E.total_chron.toFixed(1)}),c.jsx("span",{className:"lb-num-col mono lb-flourishing",children:E.flourishing.toFixed(1)}),c.jsxs("span",{className:"lb-num-col",children:[c.jsx("span",{className:"mono",children:E.ip_count}),E.ip_domains?.length>0&&c.jsxs("span",{className:"lb-ip-domains",children:[E.ip_domains.length," domains"]})]})]},E.id))]}),L.length===0&&c.jsxs("div",{className:"empty-state",children:[c.jsx("h3",{children:"No entries yet"}),c.jsx("p",{children:"Complete productions to build scores and climb the board."})]}),c.jsx("style",{children:`
        .leaderboard-table {
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          overflow: hidden;
          background: white;
        }
        .lb-header {
          display: flex;
          align-items: center;
          padding: 0.75rem 1.25rem;
          background: var(--paper-warm);
          border-bottom: 1px solid var(--border);
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
        }
        .lb-row {
          display: flex;
          align-items: center;
          padding: 0.75rem 1.25rem;
          border-bottom: 1px solid var(--border-light);
          transition: background 0.15s;
          cursor: pointer;
        }
        .lb-row:last-child { border-bottom: none; }
        .lb-row:hover { background: var(--paper-warm); }
        .lb-rank {
          width: 40px;
          flex-shrink: 0;
          font-family: 'JetBrains Mono', monospace;
          font-weight: 500;
          color: var(--ink-lighter);
          font-size: 0.85rem;
        }
        .lb-name-col {
          flex: 2;
          display: flex;
          flex-direction: column;
          gap: 0.1rem;
          min-width: 0;
        }
        .lb-name {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 0.95rem;
        }
        .lb-practice {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .lb-role-col {
          width: 100px;
          flex-shrink: 0;
        }
        .lb-num-col {
          width: 100px;
          flex-shrink: 0;
          text-align: right;
          font-size: 0.85rem;
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 0.1rem;
        }
        .lb-flourishing {
          font-weight: 600;
          color: var(--accent-dark);
        }
        .lb-ip-domains {
          font-size: 0.65rem;
          color: var(--ink-lighter);
          font-family: 'Inter', sans-serif;
        }
        .badge-principal {
          background: var(--ink);
          color: white;
        }
        .badge-talent {
          background: var(--paper-warm);
          color: var(--ink-lighter);
        }
        .mono {
          font-family: 'JetBrains Mono', monospace;
        }
      `})]})}function vp({talentId:j,onBack:w,onOpenProject:L}){const[r,b]=G.useState(null),[H,B]=G.useState(!0);return G.useEffect(()=>{fetch(`/api/roster/${j}`).then(D=>D.json()).then(D=>{b(D),B(!1)}).catch(()=>B(!1))},[j]),H?c.jsx("div",{className:"loading",children:"Loading profile..."}):r?c.jsxs("div",{className:"detail-page",children:[c.jsx("button",{className:"btn btn-back",onClick:w,children:"← Back to Roster"}),c.jsx("div",{className:"detail-header",children:c.jsxs("div",{style:{display:"flex",justifyContent:"space-between",alignItems:"flex-start"},children:[c.jsxs("div",{children:[c.jsx("h2",{children:r.name}),c.jsx("div",{className:"talent-detail-practice",children:r.domains_of_practice.join(" / ")})]}),c.jsx("span",{className:`tag ${r.availability==="available"?"available":"on-production"}`,children:r.availability==="available"?"Available":r.availability.replace("_"," ")})]})}),c.jsx("div",{className:"detail-section",children:c.jsx("p",{className:"detail-bio",children:r.bio})}),r.approach&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Approach"}),c.jsx("div",{className:"approach-block",children:c.jsx("p",{children:r.approach})})]}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Body of Work"}),r.body_of_work.map((D,E)=>c.jsxs("div",{className:"work-item",children:[c.jsx("div",{className:"work-item-title",children:D.title}),c.jsxs("div",{className:"work-item-meta",children:[D.year&&c.jsx("span",{children:D.year}),D.medium&&c.jsxs("span",{children:[" · ",D.medium]})]}),c.jsx("div",{className:"work-item-desc",children:D.description})]},E))]}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Capabilities"}),c.jsx("div",{className:"tags",style:{gap:"0.5rem"},children:r.capabilities.map((D,E)=>c.jsx("span",{className:"tag",style:{fontSize:"0.85rem",padding:"0.25rem 0.65rem"},children:D},E))})]}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Resonance Tags"}),c.jsx("div",{className:"tags",children:r.resonance_tags.map(D=>c.jsx("span",{className:"tag",children:D},D))})]}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Production History"}),c.jsxs("div",{className:"talent-detail-scores",children:[c.jsxs("div",{className:"td-score-card",children:[c.jsx("div",{className:"td-score-label",children:"Cosm Earned"}),c.jsx("div",{className:"td-score-value cosm",children:r.total_cosm.toFixed(1)})]}),c.jsxs("div",{className:"td-score-card",children:[c.jsx("div",{className:"td-score-label",children:"Chron Earned"}),c.jsx("div",{className:"td-score-value chron",children:r.total_chron.toFixed(1)})]}),c.jsxs("div",{className:"td-score-card",children:[c.jsx("div",{className:"td-score-label",children:"Productions"}),c.jsx("div",{className:"td-score-value",children:r.productions_completed.length})]})]}),r.productions_completed.length===0&&c.jsx("p",{style:{color:"var(--ink-lighter)",marginTop:"0.5rem",fontSize:"0.9rem"},children:"No productions completed yet. Available for team assembly."})]}),c.jsx("style",{children:`
        .talent-detail-practice {
          font-size: 0.9rem;
          color: var(--accent-dark);
          font-weight: 500;
          text-transform: uppercase;
          letter-spacing: 0.04em;
          margin-top: 0.25rem;
        }
        .approach-block {
          padding: 1.25rem;
          background: var(--paper-warm);
          border-radius: var(--radius-md);
          border-left: 3px solid var(--accent);
        }
        .approach-block p {
          font-size: 1rem;
          line-height: 1.7;
          color: var(--ink-light);
          font-style: italic;
        }
        .talent-detail-scores {
          display: flex;
          gap: 1rem;
        }
        .td-score-card {
          padding: 1rem 1.5rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          text-align: center;
        }
        .td-score-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
          margin-bottom: 0.25rem;
        }
        .td-score-value {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.5rem;
          font-weight: 600;
        }
        .td-score-value.cosm { color: var(--domes-color); }
        .td-score-value.chron { color: var(--spheres-color); }
      `})]}):c.jsx("div",{className:"empty-state",children:c.jsx("h3",{children:"Talent not found"})})}function gp({principalId:j,onBack:w,onOpenProject:L}){const[r,b]=G.useState(null),[H,B]=G.useState(!0);return G.useEffect(()=>{fetch(`/api/principals/${j}`).then(D=>D.json()).then(D=>{b(D),B(!1)}).catch(()=>B(!1))},[j]),H?c.jsx("div",{className:"loading",children:"Loading principal..."}):r?c.jsxs("div",{className:"detail-page",children:[c.jsx("button",{className:"btn btn-back",onClick:w,children:"← Back to Principals"}),c.jsx("div",{className:"detail-header",children:c.jsxs("div",{style:{display:"flex",alignItems:"center",gap:"1rem"},children:[c.jsx("h2",{children:r.name}),r.game_type&&c.jsx("span",{className:`badge badge-${r.game_type}`,style:{fontSize:"0.8rem",padding:"0.3rem 0.8rem"},children:r.game_type.toUpperCase()})]})}),c.jsx("div",{className:"detail-section",children:c.jsx("p",{className:"detail-bio",children:r.bio})}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Vision"}),c.jsx("div",{className:"principal-vision-block",children:c.jsx("p",{children:r.vision})})]}),r.signature_style&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Signature Style"}),c.jsx("div",{className:"signature-block",children:c.jsxs("p",{children:['"',r.signature_style,'"']})})]}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Body of Work"}),r.body_of_work.map((D,E)=>c.jsxs("div",{className:"work-item",children:[c.jsx("div",{className:"work-item-title",children:D.title}),c.jsxs("div",{className:"work-item-meta",children:[D.year&&c.jsx("span",{children:D.year}),D.medium&&c.jsxs("span",{children:[" · ",D.medium]})]}),c.jsx("div",{className:"work-item-desc",children:D.description})]},E))]}),c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Production Record"}),c.jsxs("div",{className:"principal-stats",children:[c.jsxs("div",{className:"td-score-card",children:[c.jsx("div",{className:"td-score-label",children:"Productions Led"}),c.jsx("div",{className:"td-score-value",children:r.productions_led.length})]}),c.jsxs("div",{className:"td-score-card",children:[c.jsx("div",{className:"td-score-label",children:"Total Cosm"}),c.jsx("div",{className:"td-score-value cosm",children:r.total_cosm.toFixed(1)})]}),c.jsxs("div",{className:"td-score-card",children:[c.jsx("div",{className:"td-score-label",children:"Total Chron"}),c.jsx("div",{className:"td-score-value chron",children:r.total_chron.toFixed(1)})]})]}),r.productions_led.length===0&&c.jsx("p",{style:{color:"var(--ink-lighter)",marginTop:"0.75rem",fontSize:"0.9rem"},children:"No productions led yet. Ready to attach to a project."})]}),c.jsxs("div",{className:"detail-section",children:[c.jsxs("h3",{children:["What a ",r.name," ",r.game_type==="spheres"?"Sphere":"Dome"," Looks Like"]}),c.jsx("div",{className:"what-it-looks-like",children:c.jsx("p",{children:r.game_type==="domes"?`A ${r.name} Dome — where ${r.signature_style?.toLowerCase()||r.vision.slice(0,80).toLowerCase()}. The principal's name goes on the production. Their reputation attracts talent to the roster. Their completed productions on domes.cc become portfolio pieces that attract other principals.`:`A ${r.name} Sphere — where ${r.signature_style?.toLowerCase()||r.vision.slice(0,80).toLowerCase()}. The principal's name goes on the production. Their reputation attracts talent to the roster. Their completed productions on spheres.land become portfolio pieces that attract other principals.`})})]}),c.jsx("style",{children:`
        .principal-vision-block {
          padding: 1.5rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-md);
        }
        .principal-vision-block p {
          font-size: 1.05rem;
          line-height: 1.7;
          font-style: italic;
        }
        .signature-block {
          padding: 1.25rem;
          background: var(--paper-warm);
          border-left: 3px solid var(--accent);
          border-radius: var(--radius-sm);
        }
        .signature-block p {
          font-size: 1rem;
          line-height: 1.6;
          color: var(--ink-light);
          font-style: italic;
        }
        .principal-stats {
          display: flex;
          gap: 1rem;
        }
        .td-score-card {
          padding: 1rem 1.5rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          text-align: center;
        }
        .td-score-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
          margin-bottom: 0.25rem;
        }
        .td-score-value {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.5rem;
          font-weight: 600;
        }
        .td-score-value.cosm { color: var(--domes-color); }
        .td-score-value.chron { color: var(--spheres-color); }
        .what-it-looks-like {
          padding: 1.25rem;
          background: var(--cream);
          border-radius: var(--radius-md);
        }
        .what-it-looks-like p {
          font-size: 0.95rem;
          line-height: 1.7;
          color: var(--ink-light);
        }
      `})]}):c.jsx("div",{className:"empty-state",children:c.jsx("h3",{children:"Principal not found"})})}const Od={development:"Development",pre_production:"Pre-Production",production:"Production",post_production:"Post-Production",distribution:"Distribution"},ds=["development","pre_production","production","post_production","distribution"];function yp({projectId:j,onBack:w,onOpenTalent:L,onOpenPrincipal:r}){const[b,H]=G.useState(null),[B,D]=G.useState(null),[E,h]=G.useState([]),[O,A]=G.useState(!1),[W,U]=G.useState(""),[se,_e]=G.useState(!0),[tl,q]=G.useState(null),[be,ve]=G.useState(!1),[ke,nl]=G.useState(!1),[qe,P]=G.useState(!1),[je,$e]=G.useState(null),[Ue,Ke]=G.useState(null),[Re,Tl]=G.useState(null),we=()=>{fetch(`/api/projects/${j}`).then(y=>y.json()).then(y=>{H(y.project),D(y.team),_e(!1)}).catch(()=>_e(!1))};G.useEffect(()=>{we(),fetch("/api/principals").then(y=>y.json()).then(y=>h(y.principals)).catch(()=>{})},[j]);const il=async()=>{A(!0);const y=new URLSearchParams({team_size:"6"});W&&y.set("principal_id",W),await fetch(`/api/projects/${j}/assemble?${y}`,{method:"POST"}),we(),A(!1)},N=async()=>{ve(!0);try{const X=await(await fetch(`/api/projects/${j}/start`,{method:"POST"})).json();X.stage_output&&q(X.stage_output),we()}catch(y){console.error("Start failed:",y)}ve(!1)},R=async()=>{ve(!0),q(null);try{const X=await(await fetch(`/api/projects/${j}/advance`,{method:"POST"})).json();X.stage_output&&q(X.stage_output),we()}catch(y){console.error("Advance failed:",y)}ve(!1)},k=async()=>{nl(!0);try{await fetch(`/api/projects/${j}/replay`,{method:"POST"}),q(null),$e(null),Ke(null),Tl(null),we()}catch(y){console.error("Replay failed:",y)}nl(!1)},ue=async()=>{P(!0),$e(null),Ke(null),Tl(null);try{const y=new URLSearchParams({team_size:"6"});W&&y.set("principal_id",W);const J=await(await fetch(`/api/projects/${j}/play?${y}`,{method:"POST"})).json();J.error?console.error("Play failed:",J.error):($e(J),Ke(J.final_scores),J.stages?.length>0&&q(J.stages[J.stages.length-1])),we(),d()}catch(y){console.error("Play failed:",y)}P(!1)},re=()=>{fetch(`/api/projects/${j}/scores`).then(y=>y.json()).then(y=>{y.dimensions&&Ke(y)}).catch(()=>{})},d=()=>{fetch(`/api/projects/${j}/files`).then(y=>y.json()).then(y=>{y.files&&Tl(y.files)}).catch(()=>{})};if(G.useEffect(()=>{b?.stage_log?.length>0&&re(),(b?.status==="completed"||b?.status==="published")&&d()},[b?.stage_log?.length,b?.status]),se)return c.jsx("div",{className:"loading",children:"Loading project..."});if(!b)return c.jsx("div",{className:"empty-state",children:c.jsx("h3",{children:"Project not found"})});const T=b.game_type==="domes",C=b.current_stage?ds.indexOf(b.current_stage):-1,M=tl||(b.stage_log?.length>0?b.stage_log[b.stage_log.length-1]:null);return c.jsxs("div",{className:"detail-page",style:{maxWidth:"1000px"},children:[c.jsx("button",{className:"btn btn-back",onClick:w,children:"← Back to Projects"}),c.jsx("div",{className:"detail-header",children:c.jsxs("div",{style:{display:"flex",justifyContent:"space-between",alignItems:"flex-start"},children:[c.jsxs("div",{children:[c.jsx("h2",{children:b.title}),c.jsxs("div",{style:{display:"flex",gap:"0.5rem",marginTop:"0.35rem",alignItems:"center"},children:[c.jsx("span",{className:`badge badge-${b.game_type}`,children:b.game_type.toUpperCase()}),c.jsx("span",{className:`badge badge-status ${b.status}`,children:b.status.replace("_"," ")}),b.production_number>1&&c.jsxs("span",{className:"badge",style:{background:"var(--accent-light)",color:"var(--accent-dark)"},children:["Production #",b.production_number]})]})]}),(b.cosm_score>0||b.chron_score>0)&&c.jsxs("div",{className:"score-inline",children:[c.jsxs("div",{children:[c.jsx("div",{className:"score-label",children:"Cosm"}),c.jsx("div",{className:"score-value cosm",children:b.cosm_score.toFixed(1)})]}),c.jsxs("div",{children:[c.jsx("div",{className:"score-label",children:"Chron"}),c.jsx("div",{className:"score-value chron",children:b.chron_score.toFixed(1)})]})]})]})}),Ue&&Ue.dimensions&&c.jsxs("div",{className:"detail-section",children:[c.jsxs("h3",{children:[Ue.score_type==="cosm"?"Cosm":"Chron"," Dimensions"]}),c.jsx("div",{className:"dim-grid",children:Object.entries(Ue.dimension_details||{}).map(([y,X])=>c.jsxs("div",{className:`dim-card ${y===Ue.weakest?"weakest":""} ${y===Ue.strongest?"strongest":""}`,children:[c.jsx("div",{className:"dim-label",children:X.label}),c.jsx("div",{className:"dim-score",children:X.score}),c.jsx("div",{className:"dim-bar-bg",children:c.jsx("div",{className:"dim-bar-fill",style:{width:`${X.score}%`}})}),Ue.stage_deltas?.[y]>0&&c.jsxs("div",{className:"dim-delta",children:["+",Ue.stage_deltas[y]]}),y===Ue.weakest&&c.jsx("div",{className:"dim-tag dim-tag-weak",children:"weakest"}),y===Ue.strongest&&c.jsx("div",{className:"dim-tag dim-tag-strong",children:"strongest"})]},y))}),c.jsxs("div",{className:"dim-total",children:[c.jsxs("span",{className:"dim-total-label",children:["Total ",Ue.score_type==="cosm"?"Cosm":"Chron"]}),c.jsx("span",{className:"dim-total-value",children:Ue.total}),c.jsx("span",{className:"dim-total-note",children:"= minimum across all dimensions"})]})]}),Re&&Re.length>0&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Production Files"}),c.jsx("div",{className:"files-grid",children:Re.map(y=>c.jsxs("a",{href:y.url,download:!0,className:"file-card",children:[c.jsx("div",{className:"file-icon",children:y.filename.endsWith(".json")?"{}":"#"}),c.jsxs("div",{className:"file-info",children:[c.jsx("div",{className:"file-name",children:y.filename}),c.jsx("div",{className:"file-type",children:y.key.replace(/_/g," ")})]})]},y.key))})]}),je&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Production Complete"}),c.jsxs("div",{className:"game-result-card",children:[c.jsx("div",{className:"gr-summary",children:je.summary}),je.sources_cited?.length>0&&c.jsxs("div",{className:"gr-sources",children:[c.jsxs("div",{className:"gr-sources-label",children:["Sources Cited (",je.sources_cited.length,")"]}),je.sources_cited.slice(0,8).map((y,X)=>c.jsxs("div",{className:"gr-source",children:[c.jsx("span",{className:"gr-source-type",children:y.type.replace(/_/g," ")}),c.jsx("span",{className:"gr-source-title",children:y.title})]},X)),je.sources_cited.length>8&&c.jsxs("div",{className:"gr-source-more",children:["+ ",je.sources_cited.length-8," more sources in the full report"]})]})]})]}),T&&b.character&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Character Brief"}),c.jsxs("div",{className:"brief-card",children:[c.jsx("div",{className:"brief-name",children:b.character.name}),c.jsxs("div",{className:"brief-source",children:["From ",c.jsx("em",{children:b.character.source}),c.jsx("div",{className:"brief-citation",children:b.character.source_citation})]}),c.jsxs("div",{className:"brief-block",children:[c.jsx("div",{className:"brief-label",children:"Situation"}),c.jsx("p",{children:b.character.situation})]}),c.jsxs("div",{className:"brief-block",children:[c.jsx("div",{className:"brief-label",children:"Full Landscape"}),c.jsx("p",{children:b.character.full_landscape})]}),c.jsxs("div",{className:"brief-block highlight",children:[c.jsx("div",{className:"brief-label",children:"Production Challenge"}),c.jsx("p",{children:b.character.production_challenge})]}),c.jsxs("div",{className:"brief-tags-row",children:[c.jsxs("div",{children:[c.jsx("div",{className:"brief-label",style:{marginBottom:"0.35rem"},children:"Key Systems"}),c.jsx("div",{className:"tags",children:b.character.key_systems.map(y=>c.jsx("span",{className:"tag",children:y},y))})]}),c.jsxs("div",{children:[c.jsx("div",{className:"brief-label",style:{marginBottom:"0.35rem"},children:"Flourishing Dimensions"}),c.jsx("div",{className:"tags",children:b.character.flourishing_dimensions.map(y=>c.jsx("span",{className:"tag domes",children:y},y))})]})]})]})]}),!T&&b.parcel&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Parcel Brief"}),c.jsxs("div",{className:"brief-card",children:[c.jsx("div",{className:"brief-name",children:b.parcel.address}),c.jsxs("div",{className:"brief-source",children:[b.parcel.neighborhood,", ",b.parcel.city," · ",b.parcel.zoning," · ",c.jsxs("span",{className:"mono",children:[b.parcel.lot_size_sqft.toLocaleString()," sqft"]})]}),c.jsxs("div",{className:"brief-block",children:[c.jsx("div",{className:"brief-label",children:"History"}),c.jsx("p",{children:b.parcel.history})]}),c.jsxs("div",{className:"brief-block highlight",children:[c.jsx("div",{className:"brief-label",children:"Activation Opportunity"}),c.jsx("p",{children:b.parcel.opportunity})]}),c.jsxs("div",{className:"brief-block",children:[c.jsx("div",{className:"brief-label",children:"Community Context"}),c.jsx("p",{children:b.parcel.community_context})]}),c.jsxs("div",{children:[c.jsx("div",{className:"brief-label",style:{marginBottom:"0.35rem"},children:"Constraints"}),c.jsx("div",{className:"tags",children:b.parcel.constraints.map((y,X)=>c.jsx("span",{className:"tag",children:y},X))})]})]})]}),b.current_stage&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Production Pipeline"}),c.jsx("div",{className:"stage-progress",children:ds.map((y,X)=>c.jsxs("div",{className:`stage-step ${X<=C?"done":""} ${b.current_stage===y?"current":""}`,children:[c.jsx("div",{className:"stage-step-dot"}),c.jsx("span",{className:"stage-step-label",children:Od[y]})]},y))}),b.status==="in_production"&&c.jsx("button",{className:"btn btn-primary",style:{marginTop:"1rem"},onClick:R,disabled:be,children:be?"Playing...":C<4?`Play ${Od[ds[C+1]]}`:"Complete Production"})]}),M&&c.jsxs("div",{className:"detail-section",children:[c.jsxs("h3",{children:["Stage Output: ",M.stage_name]}),c.jsxs("div",{className:"stage-output-card",children:[c.jsx("div",{className:"stage-focus",children:M.focus}),M.prior_art?.length>0&&c.jsxs("div",{className:"prior-art-section",children:[c.jsxs("div",{className:"pa-header",children:[c.jsx("span",{className:"pa-label",children:"Prior Art Available"}),c.jsxs("span",{className:"pa-count",children:[M.prior_art.length," deliverables from previous productions"]})]}),M.prior_art_referenced?.length>0&&c.jsxs("div",{className:"pa-used",children:["Building on ",M.prior_art_referenced.length," prior deliverable",M.prior_art_referenced.length>1?"s":"",":",M.prior_art_referenced.map((y,X)=>c.jsxs("div",{className:"pa-ref",children:[c.jsx("span",{className:"pa-ref-icon",children:"↪"}),c.jsxs("span",{children:[y.title," (",y.practitioner_name,")"]})]},X))]})]}),c.jsxs("div",{className:"deliverables-section",children:[c.jsxs("div",{className:"del-header",children:[c.jsxs("span",{className:"del-count",children:[M.deliverable_count," Deliverables"]}),c.jsxs("span",{className:"del-ip",children:[M.ip_count," IP Items Generated"]})]}),M.deliverables?.map((y,X)=>c.jsxs("div",{className:`deliverable-card ${y.is_unlikely?"unlikely":""}`,onClick:()=>y.talent_id&&L(y.talent_id),style:{cursor:y.talent_id?"pointer":"default"},children:[c.jsxs("div",{className:"del-top",children:[c.jsx("span",{className:"del-talent",children:y.talent_name}),c.jsx("span",{className:"del-practice",children:y.practice}),y.is_unlikely&&c.jsx("span",{className:"del-unlikely-badge",children:"Unlikely Collision"})]}),c.jsx("div",{className:"del-title",children:y.title}),y.work_referenced?.length>0&&c.jsxs("div",{className:"del-work-refs",children:["Drawing on: ",y.work_referenced.map((J,Ye)=>c.jsxs("span",{className:"del-work-ref",children:['"',J.title,'" (',J.medium,J.year?`, ${J.year}`:"",")"]},Ye))]}),c.jsx("div",{className:"del-desc",children:y.description}),c.jsxs("div",{className:"del-meta",children:[c.jsx("span",{className:`tag ${y.ip_domain==="policy"?"":y.ip_domain==="entertainment"?"domes":"spheres"}`,children:y.ip_domain?.replace("_"," ")}),y.built_on&&c.jsx("span",{className:"del-built-on",children:"Builds on prior art"})]})]},X))]}),c.jsxs("div",{className:"stage-scores",children:[c.jsxs("div",{className:"stage-score-item",children:[c.jsx("span",{className:"ss-label",children:"Cosm"}),c.jsxs("span",{className:"ss-value cosm",children:["+",M.cosm_delta]})]}),c.jsxs("div",{className:"stage-score-item",children:[c.jsx("span",{className:"ss-label",children:"Chron"}),c.jsxs("span",{className:"ss-value chron",children:["+",M.chron_delta]})]}),M.unlikely_count>0&&c.jsxs("div",{className:"stage-score-item",children:[c.jsx("span",{className:"ss-label",children:"Unlikely"}),c.jsx("span",{className:"ss-value unlikely",children:M.unlikely_count})]}),M.prior_art_used>0&&c.jsxs("div",{className:"stage-score-item",children:[c.jsx("span",{className:"ss-label",children:"Prior Art"}),c.jsxs("span",{className:"ss-value prior",children:["+",M.prior_art_used," refs"]})]})]})]})]}),b.stage_log?.length>1&&c.jsxs("div",{className:"detail-section",children:[c.jsxs("h3",{children:["Production Log (",b.stage_log.length," stages)"]}),c.jsx("div",{className:"stage-log",children:b.stage_log.map((y,X)=>c.jsxs("div",{className:"log-entry",onClick:()=>q(y),style:{cursor:"pointer"},children:[c.jsx("div",{className:"log-stage",children:y.stage_name}),c.jsxs("div",{className:"log-stats",children:[c.jsxs("span",{children:[y.deliverable_count," deliverables"]}),c.jsxs("span",{children:[y.ip_count," IP"]}),y.unlikely_count>0&&c.jsxs("span",{className:"log-unlikely",children:[y.unlikely_count," unlikely"]}),c.jsxs("span",{className:"log-cosm",children:["+",y.cosm_delta," Cosm"]}),c.jsxs("span",{className:"log-chron",children:["+",y.chron_delta," Chron"]})]})]},X))})]}),B&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Assembled Team"}),c.jsxs("div",{className:"project-team-principal",onClick:()=>r(B.principal_id),style:{cursor:"pointer"},children:[c.jsx("div",{className:"ptp-label",children:"PRINCIPAL"}),c.jsx("div",{className:"ptp-name",children:B.principal_name})]}),c.jsx("div",{className:"team-strength-box",children:c.jsx("p",{children:B.team_strength})}),B.unlikely_collisions?.length>0&&c.jsxs("div",{style:{marginBottom:"1rem"},children:[c.jsx("div",{className:"brief-label",style:{marginBottom:"0.35rem"},children:"Unlikely Collisions"}),B.unlikely_collisions.map((y,X)=>c.jsx("p",{style:{fontSize:"0.85rem",fontStyle:"italic",color:"var(--accent-dark)",marginBottom:"0.25rem"},children:y},X))]}),c.jsx("div",{className:"team-members-list",children:B.members?.map(y=>c.jsxs("div",{className:"team-member-row",onClick:()=>L(y.talent_id),children:[c.jsxs("div",{className:"tmr-left",children:[c.jsx("span",{className:"tmr-name",children:y.talent_name}),c.jsx("span",{className:"tmr-reasoning",children:y.reasoning.split("|")[0].trim()})]}),c.jsxs("div",{className:"tmr-right",children:[c.jsx("span",{className:"tmr-score",children:y.resonance_score.toFixed(0)}),c.jsx("div",{className:"resonance-bar-container",style:{width:"80px"},children:c.jsx("div",{className:"resonance-bar",style:{width:`${y.resonance_score}%`}})})]})]},y.talent_id))})]}),b.status==="sourced"&&c.jsxs("div",{className:"detail-section",children:[c.jsx("h3",{children:"Play Game"}),c.jsx("p",{style:{color:"var(--ink-lighter)",marginBottom:"1rem",fontSize:"0.9rem"},children:b.production_number>1?`Production #${b.production_number} — a new team gets the same brief. Prior art from previous productions is available.`:"Select a principal or let the agent recommend one. Play runs all 5 stages and generates real deliverable files."}),c.jsxs("div",{style:{display:"flex",flexWrap:"wrap",gap:"0.5rem",marginBottom:"1rem"},children:[c.jsx("div",{className:`filter-btn ${W===""?"active":""}`,onClick:()=>U(""),style:{cursor:"pointer"},children:"Agent's Choice"}),E.filter(y=>!b.game_type||!y.game_type||y.game_type===b.game_type).map(y=>c.jsx("div",{className:`filter-btn ${W===y.principal_id?"active":""}`,onClick:()=>U(y.principal_id),style:{cursor:"pointer"},children:y.name},y.principal_id))]}),c.jsxs("div",{style:{display:"flex",gap:"0.75rem"},children:[c.jsx("button",{className:"btn btn-primary play-btn",onClick:ue,disabled:qe,children:qe?"Playing all 5 stages...":`Play Full ${b.game_type==="domes"?"DOMES":"SPHERES"} Game`}),c.jsx("button",{className:"btn btn-secondary",onClick:il,disabled:O,children:O?"Assembling...":"Assemble Only"})]})]}),b.status==="assembling"&&B&&c.jsxs("div",{className:"detail-section",children:[c.jsx("button",{className:"btn btn-primary",onClick:N,disabled:be,children:be?"Starting...":"Start Production"}),c.jsx("p",{style:{color:"var(--ink-lighter)",marginTop:"0.5rem",fontSize:"0.85rem"},children:"Starting production begins with Development — the team produces their first deliverables."})]}),(b.status==="completed"||b.status==="published")&&c.jsx("div",{className:"detail-section",children:c.jsxs("div",{className:"replay-section",children:[c.jsx("h3",{style:{marginBottom:"0.5rem"},children:"New Production Run"}),c.jsxs("p",{style:{color:"var(--ink-lighter)",fontSize:"0.9rem",marginBottom:"1rem"},children:["Run this project again with a different team and principal. The new team will see all IP from Production #",b.production_number," as prior art and decide whether to build on it or diverge."]}),c.jsx("button",{className:"btn btn-secondary",onClick:k,disabled:ke,children:ke?"Resetting...":`Start Production #${b.production_number+1}`})]})}),c.jsx("style",{children:`
        .brief-card {
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .brief-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.3rem;
          font-weight: 600;
        }
        .brief-source {
          font-size: 0.9rem;
          color: var(--ink-lighter);
        }
        .brief-citation {
          font-size: 0.8rem;
          color: var(--ink-lighter);
          margin-top: 0.25rem;
          font-style: italic;
        }
        .brief-block {
          padding: 1rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
        }
        .brief-block.highlight {
          background: var(--cream);
          border-left: 3px solid var(--accent);
        }
        .brief-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
          margin-bottom: 0.35rem;
        }
        .brief-block p {
          font-size: 0.95rem;
          line-height: 1.6;
          color: var(--ink-light);
        }
        .brief-tags-row {
          display: flex;
          gap: 2rem;
          flex-wrap: wrap;
        }
        .stage-progress {
          display: flex;
          gap: 0;
          align-items: center;
        }
        .stage-step {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.5rem 1rem;
          border-bottom: 2px solid var(--border-light);
          flex: 1;
        }
        .stage-step.done {
          border-bottom-color: var(--accent);
        }
        .stage-step.current {
          border-bottom-color: var(--ink);
          border-bottom-width: 3px;
        }
        .stage-step-dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: var(--border);
          flex-shrink: 0;
        }
        .stage-step.done .stage-step-dot { background: var(--accent); }
        .stage-step.current .stage-step-dot { background: var(--ink); box-shadow: 0 0 0 3px rgba(26,26,26,0.15); }
        .stage-step-label {
          font-size: 0.75rem;
          font-weight: 500;
          color: var(--ink-lighter);
        }
        .stage-step.current .stage-step-label { color: var(--ink); font-weight: 600; }

        /* Stage Output */
        .stage-output-card {
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 1.5rem;
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .stage-focus {
          font-size: 1rem;
          font-style: italic;
          color: var(--ink-light);
          padding-bottom: 1rem;
          border-bottom: 1px solid var(--border-light);
        }

        /* Prior Art */
        .prior-art-section {
          background: var(--cream);
          border: 1px solid var(--accent-light);
          border-radius: var(--radius-sm);
          padding: 1rem;
        }
        .pa-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;
        }
        .pa-label {
          font-size: 0.75rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
        }
        .pa-count {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .pa-used {
          font-size: 0.85rem;
          color: var(--ink-light);
          margin-top: 0.5rem;
        }
        .pa-ref {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          padding: 0.25rem 0;
          font-size: 0.85rem;
          color: var(--accent-dark);
          font-style: italic;
        }
        .pa-ref-icon {
          font-size: 1rem;
        }

        /* Deliverables */
        .deliverables-section {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }
        .del-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .del-count {
          font-size: 0.8rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-light);
        }
        .del-ip {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-weight: 500;
        }
        .deliverable-card {
          padding: 1rem 1.25rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
          border-left: 3px solid var(--accent-light);
          transition: all 0.15s;
        }
        .deliverable-card:hover {
          border-left-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .deliverable-card.unlikely {
          border-left-color: var(--domes-color);
          background: var(--domes-bg);
        }
        .del-top {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.35rem;
        }
        .del-talent {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 0.95rem;
        }
        .del-practice {
          font-size: 0.75rem;
          color: var(--ink-lighter);
          padding: 0.1rem 0.4rem;
          background: white;
          border-radius: 20px;
          border: 1px solid var(--border-light);
        }
        .del-unlikely-badge {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--domes-color);
          padding: 0.1rem 0.5rem;
          background: white;
          border-radius: 20px;
          border: 1px solid var(--domes-light);
        }
        .del-title {
          font-weight: 600;
          font-size: 0.95rem;
          margin-bottom: 0.35rem;
          color: var(--ink);
        }
        .del-work-refs {
          font-size: 0.8rem;
          color: var(--accent-dark);
          font-style: italic;
          margin-bottom: 0.5rem;
          line-height: 1.4;
        }
        .del-work-ref {
          display: inline;
        }
        .del-work-ref + .del-work-ref::before {
          content: ' and ';
          font-style: normal;
          color: var(--ink-lighter);
        }
        .del-desc {
          font-size: 0.85rem;
          color: var(--ink-light);
          line-height: 1.6;
          margin-bottom: 0.5rem;
        }
        .del-meta {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }
        .del-built-on {
          font-size: 0.75rem;
          font-style: italic;
          color: var(--accent-dark);
        }

        /* Stage Scores */
        .stage-scores {
          display: flex;
          gap: 1.5rem;
          padding-top: 1rem;
          border-top: 1px solid var(--border-light);
        }
        .stage-score-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.15rem;
        }
        .ss-label {
          font-size: 0.65rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          color: var(--ink-lighter);
        }
        .ss-value {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.1rem;
          font-weight: 600;
        }
        .ss-value.cosm { color: var(--domes-color); }
        .ss-value.chron { color: var(--spheres-color); }
        .ss-value.unlikely { color: var(--accent-dark); }
        .ss-value.prior { color: var(--success); font-size: 0.9rem; }

        /* Stage Log */
        .stage-log {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .log-entry {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          transition: all 0.15s;
        }
        .log-entry:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .log-stage {
          font-weight: 600;
          font-size: 0.9rem;
        }
        .log-stats {
          display: flex;
          gap: 0.75rem;
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .log-unlikely {
          color: var(--accent-dark);
          font-weight: 500;
        }
        .log-cosm {
          color: var(--domes-color);
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.75rem;
        }
        .log-chron {
          color: var(--spheres-color);
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.75rem;
        }

        /* Team */
        .project-team-principal {
          padding: 1.25rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-md);
          margin-bottom: 1rem;
        }
        .ptp-label {
          font-size: 0.7rem;
          font-weight: 600;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          opacity: 0.6;
          margin-bottom: 0.25rem;
        }
        .ptp-name {
          font-family: 'Playfair Display', serif;
          font-size: 1.3rem;
          font-weight: 600;
        }
        .team-strength-box {
          padding: 1rem;
          background: var(--paper-warm);
          border-radius: var(--radius-sm);
          margin-bottom: 1rem;
        }
        .team-strength-box p {
          font-size: 0.9rem;
          color: var(--ink-light);
          line-height: 1.5;
        }
        .team-members-list {
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
        .team-member-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 0.75rem 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          cursor: pointer;
          transition: all 0.15s;
        }
        .team-member-row:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .tmr-left {
          display: flex;
          flex-direction: column;
          gap: 0.1rem;
        }
        .tmr-name {
          font-family: 'Playfair Display', serif;
          font-weight: 600;
          font-size: 0.95rem;
        }
        .tmr-reasoning {
          font-size: 0.8rem;
          color: var(--ink-lighter);
        }
        .tmr-right {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          flex-shrink: 0;
        }
        .tmr-score {
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.85rem;
          font-weight: 500;
          color: var(--accent-dark);
        }

        /* Replay */
        .replay-section {
          padding: 1.5rem;
          background: var(--paper-warm);
          border: 1px dashed var(--border);
          border-radius: var(--radius-md);
        }

        /* Play button */
        .play-btn {
          background: var(--ink) !important;
          font-size: 1rem !important;
          padding: 0.75rem 2rem !important;
        }

        /* Dimension Scores */
        .dim-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
          gap: 0.75rem;
          margin-bottom: 1rem;
        }
        .dim-card {
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          padding: 0.75rem;
          text-align: center;
          position: relative;
        }
        .dim-card.weakest { border-color: #e74c3c; border-width: 2px; }
        .dim-card.strongest { border-color: #27ae60; border-width: 2px; }
        .dim-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--ink-lighter);
          margin-bottom: 0.25rem;
        }
        .dim-score {
          font-family: 'JetBrains Mono', monospace;
          font-size: 1.5rem;
          font-weight: 700;
          color: var(--ink);
        }
        .dim-bar-bg {
          height: 4px;
          background: var(--border-light);
          border-radius: 2px;
          margin-top: 0.35rem;
          overflow: hidden;
        }
        .dim-bar-fill {
          height: 100%;
          background: var(--accent);
          border-radius: 2px;
          transition: width 0.5s ease;
        }
        .dim-card.weakest .dim-bar-fill { background: #e74c3c; }
        .dim-card.strongest .dim-bar-fill { background: #27ae60; }
        .dim-delta {
          position: absolute;
          top: 4px;
          right: 6px;
          font-size: 0.7rem;
          font-family: 'JetBrains Mono', monospace;
          color: var(--accent-dark);
        }
        .dim-tag {
          font-size: 0.6rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          margin-top: 0.35rem;
          padding: 0.1rem 0.3rem;
          border-radius: 3px;
          display: inline-block;
        }
        .dim-tag-weak { background: #fde8e8; color: #e74c3c; }
        .dim-tag-strong { background: #e8f5e9; color: #27ae60; }
        .dim-total {
          display: flex;
          align-items: baseline;
          gap: 0.75rem;
          padding: 1rem;
          background: var(--ink);
          color: white;
          border-radius: var(--radius-sm);
        }
        .dim-total-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.08em;
          opacity: 0.7;
        }
        .dim-total-value {
          font-family: 'JetBrains Mono', monospace;
          font-size: 2rem;
          font-weight: 700;
        }
        .dim-total-note {
          font-size: 0.75rem;
          opacity: 0.5;
          font-style: italic;
        }

        /* Files */
        .files-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
          gap: 0.5rem;
        }
        .file-card {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          padding: 0.75rem 1rem;
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-sm);
          text-decoration: none;
          color: var(--ink);
          transition: all 0.15s;
        }
        .file-card:hover {
          border-color: var(--accent);
          box-shadow: var(--shadow-sm);
        }
        .file-icon {
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--paper-warm);
          border-radius: 4px;
          font-family: 'JetBrains Mono', monospace;
          font-size: 0.8rem;
          font-weight: 600;
          color: var(--accent-dark);
          flex-shrink: 0;
        }
        .file-info {
          display: flex;
          flex-direction: column;
          min-width: 0;
        }
        .file-name {
          font-size: 0.8rem;
          font-weight: 500;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .file-type {
          font-size: 0.7rem;
          color: var(--ink-lighter);
          text-transform: capitalize;
        }

        /* Game Result */
        .game-result-card {
          background: white;
          border: 1px solid var(--border);
          border-radius: var(--radius-md);
          padding: 1.5rem;
        }
        .gr-summary {
          white-space: pre-wrap;
          font-size: 0.85rem;
          line-height: 1.7;
          color: var(--ink-light);
          margin-bottom: 1rem;
        }
        .gr-sources {
          padding-top: 1rem;
          border-top: 1px solid var(--border-light);
        }
        .gr-sources-label {
          font-size: 0.7rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 0.06em;
          color: var(--accent-dark);
          margin-bottom: 0.5rem;
        }
        .gr-source {
          display: flex;
          gap: 0.5rem;
          align-items: baseline;
          padding: 0.2rem 0;
          font-size: 0.8rem;
        }
        .gr-source-type {
          font-size: 0.65rem;
          font-weight: 600;
          text-transform: uppercase;
          color: var(--ink-lighter);
          padding: 0.1rem 0.3rem;
          background: var(--paper-warm);
          border-radius: 3px;
          white-space: nowrap;
        }
        .gr-source-title {
          color: var(--ink-light);
        }
        .gr-source-more {
          font-size: 0.75rem;
          font-style: italic;
          color: var(--ink-lighter);
          margin-top: 0.5rem;
        }
      `})]})}const bp=[{key:"roster",label:"Roster"},{key:"principals",label:"Principals"},{key:"projects",label:"Projects"},{key:"sourcing",label:"Sourcing"},{key:"assembly",label:"Assembly"},{key:"ip",label:"IP"},{key:"leaderboard",label:"Board"}];function xp(){const[j,w]=G.useState("roster"),[L,r]=G.useState(null),[b,H]=G.useState(null),[B,D]=G.useState(null);G.useEffect(()=>{fetch("/api/stats").then(A=>A.json()).then(r).catch(()=>{})},[j]);const E=A=>{w(A),H(null),D(null)},h=(A,W)=>{D(A),H(W)},O=()=>{H(null),D(null)};return B==="talent"&&b?c.jsxs("div",{className:"app",children:[c.jsx(Qi,{stats:L,view:j,navigateTo:E}),c.jsx("main",{children:c.jsx(vp,{talentId:b,onBack:O,onOpenProject:A=>h("project",A)})})]}):B==="principal"&&b?c.jsxs("div",{className:"app",children:[c.jsx(Qi,{stats:L,view:j,navigateTo:E}),c.jsx("main",{children:c.jsx(gp,{principalId:b,onBack:O,onOpenProject:A=>h("project",A)})})]}):B==="project"&&b?c.jsxs("div",{className:"app",children:[c.jsx(Qi,{stats:L,view:j,navigateTo:E}),c.jsx("main",{children:c.jsx(yp,{projectId:b,onBack:O,onOpenTalent:A=>h("talent",A),onOpenPrincipal:A=>h("principal",A)})})]}):c.jsxs("div",{className:"app",children:[c.jsx(Qi,{stats:L,view:j,navigateTo:E}),c.jsxs("main",{children:[j==="roster"&&c.jsx(rp,{onOpenTalent:A=>h("talent",A)}),j==="principals"&&c.jsx(fp,{onOpenPrincipal:A=>h("principal",A)}),j==="projects"&&c.jsx(op,{onOpenProject:A=>h("project",A)}),j==="sourcing"&&c.jsx(dp,{onOpenProject:A=>h("project",A)}),j==="assembly"&&c.jsx(mp,{onOpenProject:A=>h("project",A),onOpenTalent:A=>h("talent",A)}),j==="ip"&&c.jsx(hp,{}),j==="leaderboard"&&c.jsx(pp,{onOpenTalent:A=>h("talent",A),onOpenPrincipal:A=>h("principal",A)})]})]})}function Qi({stats:j,view:w,navigateTo:L}){return c.jsxs("header",{children:[c.jsxs("div",{className:"header-left",children:[c.jsxs("div",{className:"header-brand",onClick:()=>L("roster"),children:[c.jsx("h1",{className:"logo",children:"CHRON"}),c.jsx("span",{className:"logo-sub",children:"Talent Agent"})]}),j&&c.jsxs("div",{className:"header-stats",children:[c.jsxs("span",{className:"stat-pill",children:[j.roster_size," practitioners"]}),c.jsxs("span",{className:"stat-pill",children:[j.principals_count," principals"]}),c.jsxs("span",{className:"stat-pill active-pill",children:[j.active_productions," active"]})]})]}),c.jsx("nav",{children:bp.map(r=>c.jsx("button",{className:w===r.key?"active":"",onClick:()=>L(r.key),children:r.label},r.key))})]})}sp.createRoot(document.getElementById("root")).render(c.jsx(G.StrictMode,{children:c.jsx(xp,{})}));
