/* BEGIN MKDOCS TEMPLATE */
/* WARNING, DO NOT UPDATE CONTENT BETWEEN MKDOCS TEMPLATE TAG !*/
/* Modified content will be overwritten when updating.*/
"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
var SRE = require("speech-rule-engine");
global.SRE = SRE;
global.sre = Object.create(SRE);
global.sre.Engine = {
    isReady: function () {
        return SRE.engineReady();
    }
};
//# sourceMappingURL=sre-node.js.map
/* END MKDOCS TEMPLATE */
