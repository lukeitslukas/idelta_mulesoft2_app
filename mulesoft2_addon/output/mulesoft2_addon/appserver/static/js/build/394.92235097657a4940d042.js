(self.webpackChunk_splunk_ucc_ui_lib=self.webpackChunk_splunk_ucc_ui_lib||[]).push([[394],{7739:(e,t,n)=>{(()=>{"use strict";var t={n:e=>{var n=e&&e.__esModule?()=>e.default:()=>e;return t.d(n,{a:n}),n},d:(e,n)=>{for(var r in n)t.o(n,r)&&!t.o(e,r)&&Object.defineProperty(e,r,{enumerable:!0,get:n[r]})},o:(e,t)=>Object.prototype.hasOwnProperty.call(e,t),r:e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})}},r={};t.r(r),t.d(r,{default:()=>p});const a=n(96540);var o=t.n(a);const l=n(24509);var i=t.n(l);const c=n(62283);var u=new Map;u.set("outlined",(function(){return o().createElement(o().Fragment,null,o().createElement("path",{fillRule:"evenodd",clipRule:"evenodd",d:"M8.94008 2C8.11165 2 7.44008 2.67157 7.44008 3.5V9H5.47861C4.11314 9 3.45783 10.676 4.46119 11.6022L10.9824 17.6218C11.557 18.1521 12.4426 18.1521 13.0172 17.6217L19.5384 11.6022C20.5417 10.676 19.8864 9 18.5209 9H16.5553V3.5C16.5553 2.67157 15.8838 2 15.0553 2H8.94008ZM9.44008 11V4H14.5553V11H17.2421L11.9998 15.8391L6.75743 11H9.44008Z"}),o().createElement("path",{d:"M4 20C3.44772 20 3 20.4477 3 21C3 21.5523 3.44772 22 4 22H20C20.5523 22 21 21.5523 21 21C21 20.4477 20.5523 20 20 20H4Z"}))})),u.set("filled",(function(){return o().createElement(o().Fragment,null,o().createElement("path",{d:"M7.44032 3.5C7.44032 2.67157 8.1119 2 8.94032 2H15.0556C15.884 2 16.5556 2.67157 16.5556 3.5V9H18.5212C19.8867 9 20.542 10.676 19.5386 11.6022L13.0174 17.6217C12.4429 18.1521 11.5572 18.1521 10.9826 17.6218L4.46143 11.6022C3.45808 10.676 4.11338 9 5.47885 9H7.44032V3.5Z"}),o().createElement("path",{d:"M3 21C3 20.4477 3.44772 20 4 20H20C20.5523 20 21 20.4477 21 21C21 21.5523 20.5523 22 20 22H4C3.44772 22 3 21.5523 3 21Z"}))}));var f=["default","outlined","filled"],s=function(e){return"default"===e||e&&!function(e){return f.indexOf(e)>=0}(e)?"outlined":e},m=function(e){var t=e.children,n=e.variant,r=function(e,t){if(null==e)return{};var n,r,a=function(e,t){if(null==e)return{};var n,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||(a[n]=e[n]);return a}(e,t);if(Object.getOwnPropertySymbols){var o=Object.getOwnPropertySymbols(e);for(r=0;r<o.length;r++)n=o[r],t.indexOf(n)>=0||Object.prototype.propertyIsEnumerable.call(e,n)&&(a[n]=e[n])}return a}(e,["children","variant"]),l=s(n),f="arrowbroadunderbardown-".concat(l),m=(0,a.useContext)(c.IconContext),p=u.get(l);if(m&&p){var d=m.toRender;if((0,m.addIcon)(f,p()),!d)return null}return o().createElement(i(),r,t,m?o().createElement("use",{href:"#".concat(f)}):!!p&&p())};m.defaultProps={variant:"default"};const p=m;e.exports=r})()},46394:(e,t,n)=>{"use strict";n.r(t),n.d(t,{default:()=>ue});var r=n(96540),a=n(20259),o=n(65889),l=n.n(o),i=n(13700),c=n.n(i),u=n(52473),f=n.n(u),s=n(92568),m=n(73693),p=n(10670),d=n(32677),b=n(96791),y=n(5556),v=n.n(y),g=n(66930);function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function O(e){var t,n,o=e.tab,l=(t=(0,r.useState)(!0),n=2,function(e){if(Array.isArray(e))return e}(t)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],c=!0,u=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);c=!0);}catch(e){u=!0,a=e}finally{try{if(!c&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(u)throw a}}return i}}(t,n)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?h(e,t):void 0}}(t,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()),i=l[0],c=l[1],u=(0,r.useRef)(null),f=(0,p.Sb)().meta.name;return(0,r.useEffect)((function(){new Promise((function(e){"external"===o.customTab.type?import("".concat((0,g.B)(),"/custom/").concat(o.customTab.src,".js")).then((function(t){var n=t.default;e(n)})):require(["app/".concat(f,"/js/build/custom/").concat(o.customTab.src)],(function(t){return e(t)}))})).then((function(e){new e(o,u.current).render(),c(!1)}))}),[]),r.createElement(r.Fragment,null,i&&(0,a._)("Loading..."),r.createElement("div",{ref:u,style:{visibility:i?"hidden":"visible"}}))}O.propTypes={tab:v().object.isRequired};const j=O;var E,S=n(24379),w=n.n(S),A=n(15603),C=n(74042),P=n(81705),I=n(33563),T=n(36371),x=n(17467);function k(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],c=!0,u=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);c=!0);}catch(e){u=!0,a=e}finally{try{if(!c&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(u)throw a}}return i}}(e,t)||function(e,t){if(e){if("string"==typeof e)return _(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?_(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function _(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var N,L,M=s.default.div(E||(N=["\n    margin-left: 270px !important;\n    width: 150px;\n"],L||(L=N.slice(0)),E=Object.freeze(Object.defineProperties(N,{raw:{value:Object.freeze(L)}}))));function H(e){var t=e.serviceName,n=(0,r.useRef)(),o=k((0,r.useState)(null),2),l=o[0],i=o[1],c=k((0,r.useState)(!1),2),u=c[0],f=c[1],s=k((0,r.useState)({}),2),m=s[0],p=s[1];if((0,r.useEffect)((function(){(0,P.Y)({serviceName:"settings/".concat(t),handleError:!0,callbackOnError:function(e){i(e)}}).then((function(e){p(e.data.entry[0].content)}))}),[t]),l)throw l;return Object.keys(m).length?r.createElement(r.Fragment,null,r.createElement(A.A,{ref:n,page:x.hS,stanzaName:t,serviceName:"settings",mode:I.DJ,currentServiceState:m,handleFormSubmit:function(e){f(e)}}),r.createElement(M,null,r.createElement(C.OV,{className:"saveBtn",appearance:"primary",label:u?r.createElement(w(),null):(0,a._)("Save"),onClick:function(e){n.current.handleSubmit(e)},disabled:u}))):r.createElement(T.Ku,{size:"medium"})}H.propTypes={serviceName:v().string.isRequired};const z=H;var R=n(44798),D=n(32251),U=n(37668),q=n(80917),F=n(90785);function V(e){return V="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},V(e)}function Z(e,t){var n=Object.keys(e);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(e);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(e,t).enumerable}))),n.push.apply(n,r)}return n}function B(e){for(var t=1;t<arguments.length;t++){var n=null!=arguments[t]?arguments[t]:{};t%2?Z(Object(n),!0).forEach((function(t){var r,a,o,l;r=e,a=t,o=n[t],l=function(e,t){if("object"!=V(e)||!e)return e;var n=e[Symbol.toPrimitive];if(void 0!==n){var r=n.call(e,"string");if("object"!=V(r))return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return String(e)}(a),(a="symbol"==V(l)?l:l+"")in r?Object.defineProperty(r,a,{value:o,enumerable:!0,configurable:!0,writable:!0}):r[a]=o})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(n)):Z(Object(n)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(n,t))}))}return e}function $(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}function J(e){var t,n,a=e.selectedTab,o=e.updateIsPageOpen,l=(t=(0,r.useState)({open:!1}),n=2,function(e){if(Array.isArray(e))return e}(t)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],c=!0,u=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);c=!0);}catch(e){u=!0,a=e}finally{try{if(!c&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(u)throw a}}return i}}(t,n)||function(e,t){if(e){if("string"==typeof e)return $(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?$(e,t):void 0}}(t,n)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()),i=l[0],c=l[1],u=a.style===F.S;(0,r.useEffect)((function(){u&&o(!!i.open)}),[i]);return r.createElement(R.r,{value:null},u&&i.open&&r.createElement(q.A,{open:i.open,handleRequestClose:function(){c(B(B({},i),{},{open:!1}))},serviceName:a.name,stanzaName:i.stanzaName,mode:i.mode,formLabel:i.formLabel,page:x.hS}),r.createElement("div",{style:u&&i.open?{display:"none"}:{display:"block"}},r.createElement(D.A,{page:x.hS,serviceName:a.name,handleRequestModalOpen:function(){c(B(B({},i),{},{open:!0,mode:I.F9,formLabel:"Add ".concat(a.title)}))},handleOpenPageStyleDialog:function(e,t){c(B(B({},i),{},{open:!0,stanzaName:e.name,formLabel:t===I.UT?"Clone ".concat(a.title):"Update ".concat(a.title),mode:t}))}})),!u&&i.open&&r.createElement(U.A,{page:x.hS,open:i.open,handleRequestClose:function(){c(B(B({},i),{},{open:!1}))},serviceName:a.name,mode:I.F9,formLabel:i.formLabel}))}J.propTypes={selectedTab:v().object,updateIsPageOpen:v().func};const K=(0,r.memo)(J);var W=n(7739),Y=n.n(W),G=n(70181),Q=n.n(G);const X=function(e){return r.createElement(Q(),{target:"_blank",to:e.fileUrl,download:e.fileNameAfterDownload,"data-test":"downloadButton"},e.children)};var ee,te;function ne(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}const re=function(){var e=s.default.div(ee||(ee=ne(["\n        text-overflow: ellipsis;\n        overflow: hidden;\n    "]))),t=(0,s.default)(Y())(te||(te=ne(["\n        margin-right: 4px;\n    "])));return r.createElement(X,{fileUrl:(0,g.B)().replace("js/build","openapi.json"),fileNameAfterDownload:"openapi.json"},r.createElement(e,null,r.createElement(t,null),r.createElement("span",null,"OpenAPI.json")))};var ae,oe=n(38837);function le(e,t){return function(e){if(Array.isArray(e))return e}(e)||function(e,t){var n=null==e?null:"undefined"!=typeof Symbol&&e[Symbol.iterator]||e["@@iterator"];if(null!=n){var r,a,o,l,i=[],c=!0,u=!1;try{if(o=(n=n.call(e)).next,0===t){if(Object(n)!==n)return;c=!1}else for(;!(c=(r=o.call(n)).done)&&(i.push(r.value),i.length!==t);c=!0);}catch(e){u=!0,a=e}finally{try{if(!c&&null!=n.return&&(l=n.return(),Object(l)!==l))return}finally{if(u)throw a}}return i}}(e,t)||function(e,t){if(e){if("string"==typeof e)return ie(e,t);var n=Object.prototype.toString.call(e).slice(8,-1);return"Object"===n&&e.constructor&&(n=e.constructor.name),"Map"===n||"Set"===n?Array.from(e):"Arguments"===n||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n)?ie(e,t):void 0}}(e,t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()}function ie(e,t){(null==t||t>e.length)&&(t=e.length);for(var n=0,r=new Array(t);n<t;n++)r[n]=e[n];return r}var ce=(0,s.default)(f().Row)(ae||(ae=function(e,t){return t||(t=e.slice(0)),Object.freeze(Object.defineProperties(e,{raw:{value:Object.freeze(t)}}))}(["\n    padding: 5px 0px;\n\n    .dropdown {\n        text-align: right;\n    }\n\n    .input_button {\n        text-align: right;\n        margin-right: 0px;\n    }\n"])));const ue=function(){var e=(0,p.Sb)().pages.configuration,t=e.title,n=e.description,o=e.subDescription,i=e.tabs,u=i.map((function(e){return e.name})),s=le((0,r.useState)(i[0].name),2),y=s[0],v=s[1],g=le((0,r.useState)(!1),2),h=g[0],O=g[1],E=(0,m.A)();(0,r.useEffect)((function(){E&&u.includes(E.get("tab"))&&E.get("tab")!==y&&v(E.get("tab"))}),[]);var S=(0,r.useCallback)((function(e,t){var n=t.selectedTabId;v(n),O(!1)}),[y]),w=function(e){O(e)};return r.createElement(b.A,null,r.createElement("div",{style:h?{display:"none"}:{display:"block"}},r.createElement(f(),{gutter:8},r.createElement(ce,null,r.createElement(f().Column,{span:9},r.createElement(d.WI,null,(0,a._)(t)),r.createElement(d.qA,null,(0,a._)(n||"")),r.createElement(oe.A,o)),r.createElement(f().Column,{span:3,style:{textAlignLast:"right"}},r.createElement(re,null)))),r.createElement(l(),{activeTabId:y,onChange:S},i.map((function(e){return r.createElement(l().Tab,{key:e.name,label:(0,a._)(e.title),tabId:e.name})})))),i.map((function(e){return function(e){var t;return t=null!=e&&e.customTab?function(e){return r.createElement(j,{tab:e})}(e):null!=e&&e.table?r.createElement(K,{key:e.name,selectedTab:e,updateIsPageOpen:w}):r.createElement(z,{key:e.name,serviceName:e.name}),r.createElement("div",{key:e.name,style:e.name!==y?{display:"none"}:{display:"block"},id:"".concat(e.name,"Tab")},t)}(e)})),r.createElement(c(),{position:"top-right"}))}}}]);
//# sourceMappingURL=394.92235097657a4940d042.js.map