<template>
  <div class="modal" aria-labelledby="modal-title" aria-hidden="true" @click="close">
    <div class="modal-dialog" role="document" @click.prevent.stop="">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal-title">
            Burn Down Chart
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body">
          <img v-bind:src="'http://localhost:3000/api/chart/' + this.boardId" width="100%">
<!--          <img src="http://localhost:3000/api/chart/1" >-->
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="close">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {createNamespacedHelpers} from 'vuex';

const {mapState, mapGetters} = createNamespacedHelpers('board');

export default {
  name: "BurnDownChartShow",
    props: {
      boardId: {
        type: Number,
      default: null,
    },
  },
  computed: {
    boardName() {
      return this.boardData.name;
    },
    ...mapState([
      'boardData',
    ]),
    ...mapGetters(['getBoardId']),
  },
  methods:{
    close() {
      this.$router.push({
        path: `/boards/${this.boardId}`,
        query: this.$route.query,
      });
    },
  },
}
</script>

<style lang='scss' scoped>
.modal {
  display: block;
  background-color: rgba(1, 1, 1, 0.5);
}

.modal-dialog {
  z-index: 1060;
}

.edit-area {
  width: 95%;
  height: 5rem;
}

.empty-content {
  text-decoration: underline;
  cursor: pointer;
}

.card-content {
  //white-space: pre;
  //break-spaces;
}
</style>