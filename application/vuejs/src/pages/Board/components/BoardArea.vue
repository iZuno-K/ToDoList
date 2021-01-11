<template>
  <div class="board-area">
    <Draggable
        v-model="wrappedPipeLineList"
        class="board-container"
        :options="options"
    >
      <PipeLine
          v-for="pipeLine in wrappedPipeLineList"
          :pipeLine="pipeLine"
          class="pipe-line-item"
          :key="pipeLine.id"
      />
       <AddPipeLine />
    </Draggable>
    <router-view></router-view>
  </div>
</template>

<script>
import Draggable from 'vuedraggable';
import {createNamespacedHelpers} from 'vuex';
import PipeLine from './BoardArea/PipeLine';
import AddPipeLine from './BoardArea/AddPipeLine';


const {mapGetters} = createNamespacedHelpers('board');


export default {
  name: "BoardArea",
  components: {
    Draggable,
    PipeLine,
    AddPipeLine,
  },
  data() {
    return {
      options: {
        animation: 300,
        draggable: '.pipe-line-item',
      },
    };
  },
  computed: {
    wrappedPipeLineList: {
      get() {
        return this.getFilteredPipeLineList;
      },
      set(value) {
        console.log('update', value);
      },
    },
    ...mapGetters([
      'getFilteredPipeLineList',
      'getBoardId',
    ]),
  },
  methods: {},
};
</script>

<style scoped>
.board-area {
  margin: 1rem 0;
  width: 100%;
}

.board-container {
  display: flex;
}
</style>