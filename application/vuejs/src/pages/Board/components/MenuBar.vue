<template>
  <div class="board-menu-bar navbar navbar-dark bg-dark">
    <span class="navbar-brand mb-0 h1 board-name" @click="editBoard">{{ boardName }}</span>
    <span class="text-white"> {{ startDate }} to {{ endDate }}</span>
    <nav class="my-2 my-md-0 mr-md-3">
      <button type="button" class="btn btn-primary" @click="openBurnDownChart">BurnDownChart</button>
<!--      <form class="form-inline mt-2 mt-md-0" id="search-form">-->
<!--        <input name="query" class="form-control mr-3" type="text" placeholder="Search"-->
<!--               aria-label="Search">-->
<!--        <button type="button" class="btn btn-outline-danger">delete</button>-->
<!--      </form>-->
    </nav>
  </div>
</template>

<script>
import {createNamespacedHelpers} from 'vuex';

const {mapState, mapGetters} = createNamespacedHelpers('board');

export default {
  name: "MenuBar",
  data() {
    return {};
  },
  computed: {
    boardName() {
      return this.boardData.name;
    },
    startDate() {
      return this.boardData.startDate;
    },
    endDate() {
      return this.boardData.endDate;
    },
    ...mapState([
      'boardData',
    ]),
    ...mapGetters(['getBoardId']),
  },
  methods: {
    openBurnDownChart() {
      this.$router.push({
        path: `/boards/${this.getBoardId}/BurnDownChart`,
        query: this.$route.query,
      });
    },
    editBoard() {
      this.$router.push({
        path: `/boards/${this.getBoardId}/boardInfo`,
        query: this.$route.query,
      });
    },
  },
};
</script>

<style scoped>
.board-menu-bar {
  margin: 1rem 0;
  width: 100%;
}

.board-name {
  cursor: pointer;
}
</style>