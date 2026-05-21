<template>
    <div>
        <div class="boxcalculator">
            <div class="contentcalculator">
                <label class="alert title">{{ title }}</label>
                <!-- <b-form-input id="pax" :placeholder="placeholder" v-model="inputmodel"></b-form-input> -->
                <my-number class="form-control text-right" v-model="inputmodel" :precision="0"></my-number>
                <br>
                <div class="float-left">
                    <b-button id="btn1" @click="keyboardClicked('1')" class="btn-calculator empty">1</b-button>
                    <b-button id="btn2" @click="keyboardClicked('2')" class="btn-calculator empty">2</b-button>
                    <b-button id="btn3" @click="keyboardClicked('3')" class="btn-calculator empty">3</b-button>
                    <b-button id="btn4" @click="keyboardClicked('4')" class="btn-calculator empty">4</b-button>
                    <b-button id="btn5" @click="keyboardClicked('5')" class="btn-calculator empty">5</b-button>
                    <b-button id="btn6" @click="keyboardClicked('6')" class="btn-calculator empty">6</b-button>
                    <b-button id="btn7" @click="keyboardClicked('7')" class="btn-calculator empty">7</b-button>
                    <b-button id="btn8" @click="keyboardClicked('8')" class="btn-calculator empty">8</b-button>
                    <b-button id="btn9" @click="keyboardClicked('9')" class="btn-calculator empty">9</b-button>
                    <b-button id="btn0" @click="keyboardClicked('0')" class="btn-calculator empty">0</b-button>
                    <b-button id="btnDel" @click="keyboardClicked('del')" class="btn-calculator empty" style="width: 160px;"><i class="fa fa-chevron-left"></i><i class="fa fa-chevron-left"></i> Del</b-button>
                </div>
            </div>
            <div class="bottom-calculator">
                <b-button @click="cancel" class="alert back btn-normal btn-command btn-animation mt-2 mb-2 mr-2">
                    <i class="fa fa-chevron-left m-0"></i>
                    {{myLabels[0]}}
                </b-button>
                <b-button @click="save" class="primary next btn-normal btn-command btn-animation mt-2 mb-2">
                    {{myLabels[1]}}
                    <i class="fa fa-chevron-right"></i>
                </b-button>
            </div>
        </div>
    </div>
</template>
<style lang="scss" scoped>
   .btn-calculator {
       height: 50px;
       width: 75px;
       padding: 5px;
       margin: 5px;
       color: white;
   }

   .btn-command {
       height: 50px;
       width: calc(50% - 10px);
   }

    .title {
        width: 100%;
        padding: 5px;
        text-align: center;
        color: white;
        border-radius: 3px;
    }

   .contentcalculator {
       padding: 10px;
       width: 300px;
       height: 380px;
       margin: 0 auto;
       background: #2f353a;
       border-radius: 5px;
       text-align: center;
   }    

    .bottom-calculator {
       padding: 10px;
       width: 300px;
       margin: 0 auto;
       border-radius: 5px;
       text-align: center;
    }
</style>

<script>
import myNumber from "./my-number";

export default {
  name: 'boxCalculator',
  components: {myNumber},
  props: ["labels", "variants", "title", "value","placeholder","maxlength", "max" ],
  data() {
    const { labels, variants, title, value, placeholder, maxlength, max } = this;
    let myLabels = ["Back", "Next"];
    // let btnVariant = ["alert", "primary"];
    let myMaxlength = 2;
    let myMaxValue = 0;
    if (labels) myLabels = eval(labels);
    if (maxlength) myMaxlength = eval(maxlength);
    // if (variants) btnVariant = eval(variants);
    if (max) myMaxValue = eval(max);
    return { myMaxValue, myLabels, myMaxlength };
  },
  computed: {
    inputmodel: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    }
  },
  methods: {
    cancel() {
        this.$emit("cancel");
    },
    save() {
        this.$emit("save");
    },
    keyboardClicked: function(val) {
        // console.log('val ke clicked: ', val);
        if (val==='del') {
            const currVal = this.inputmodel;
            this.inputmodel = (currVal.toString().trim().length - 1)>0? currVal.toString().substring(0, (currVal.toString().trim().length - 1)):'';
        } else {
            const pax = this.inputmodel;
            const currVal = isNaN(parseInt(this.inputmodel))?0:this.inputmodel;
            const valNow = parseInt(`${currVal}${val}`, 10);
            if (this.myMaxValue > 0) {
                if (valNow.toString().trim().length <= this.myMaxlength && valNow <= this.myMaxValue) {
                    this.inputmodel = valNow;
                }
            } else {
                if (valNow.toString().trim().length <= this.myMaxlength) {
                    this.inputmodel = valNow;
                } 
            }
        } 
        // console.log('this.inputmodel ke clicked: ', this.inputmodel);
      },
  }
};
</script>