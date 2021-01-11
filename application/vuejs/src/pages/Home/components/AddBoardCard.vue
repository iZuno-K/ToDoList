<template>
  <a href="#" @click="addBoardAction">
    <div class="card bg-dark text-white">
      <div class="card-body">
        <h5 class="card-title">Add Board(+)</h5>
      </div>
    </div>
  </a>
</template>

<script>
import { createNamespacedHelpers } from 'vuex';

const { mapActions } = createNamespacedHelpers('home');


export default {
  name: 'AddBoardCard',
  methods: {
    addBoardAction() {
      const boardName = window.prompt('BoardName?');
      const startDate = window.prompt('StartDate?');
      const endDate = window.prompt('EndDate?');
      if (boardName && startDate && endDate) {
        this.addBoard({
          boardName, startDate, endDate
        });
      }
    },
    ...mapActions(['addBoard']),
  }
};
</script>
