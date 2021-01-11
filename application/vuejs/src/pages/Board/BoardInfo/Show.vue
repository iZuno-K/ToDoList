<template>
  <div class="modal" aria-labelledby="modal-title" aria-hidden="true" @click="close">
    <div class="modal-dialog" role="document" @click.prevent.stop="">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal-title">
            <span v-show="!isTitleEditing" @dblclick="startTitleEdit">
               {{ boardData.name }}
            </span>
            <span v-show="isTitleEditing">
              <input type="text" v-model="editTitle">
              <button type="button" class="btn btn-primary" @click="saveTitle">save</button>
            </span>
          </h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close" @click="close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body" v-show="!isContentEditing">
          <div v-if="boardData.name" @dblclick="startContentEdit" class="card-content">
            <table>
              <tr>
                <td>Start date</td>
                <td> : &nbsp;</td>
                <td>{{ boardData.startDate }}</td>
              </tr>
              <tr>
                <td>End date</td>
                <td> :</td>
                <td>{{ boardData.endDate }}</td>
              </tr>
            </table>
          </div>
          <p v-else @click="startContentEdit" class="empty-content">enter content.</p>
        </div>
        <div class="modal-body" v-show="isContentEditing">
          <table>
            <tr>
              <td>Start date</td>
              <td> : &nbsp;</td>
              <td><input type="text" v-model="editStartDate"></td>
            </tr>
            <tr>
              <td>End date</td>
              <td> :</td>
              <td><input type="text" v-model="editEndDate"></td>
            </tr>
          </table>
        </div>
        <button type="button" class="btn btn-primary" @click="saveContent">Save</button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-primary" @click="close">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import {createNamespacedHelpers} from 'vuex';

const {mapState, mapActions} = createNamespacedHelpers('board');
export default {
  name: 'BoardInfoShow',
    props: {
      boardId: {
        type: Number,
      default: null,
    },
  },
  computed: {
    ...mapState(['boardData']),
  },
  data() {
    return {
      isContentEditing: false,
      editContent: '',
      isTitleEditing: false,
      editTitle: '',
      editStartDate: '',
      editEndDate: '',
    };
  },
  methods: {
    close() {
      console.log("close boardInfo", this.boardId);
      this.$router.push({
        path: `/boards/${this.boardId}`,
        query: this.$route.query,
      });
    },
    startContentEdit() {
      this.isContentEditing = true;
      this.editStartDate = this.boardData.startDate;
      this.editEndDate = this.boardData.endDate;
    },
    startTitleEdit() {
      this.isTitleEditing = true;
      this.editTitle = this.boardData.name;
    },
    async saveContent() {
      this.isContentEditing = false;
      // if (this.editContent === this.focusedCard.content) return;
      await this.updateBoardContent({
        boardId: this.boardId,
        startDate: this.editStartDate,
        endDate: this.editEndDate,
      });
      this.close();
    },
    async saveTitle() {
      this.isTitleEditing = false;
      if (this.editTitle === this.boardData.name) return;
      await this.updateBoardTitle({
        boardId: this.boardId,
        name: this.editTitle,
      });
      this.close();
    },
    ...mapActions([
      'updateBoardContent',
      'updateBoardTitle',
    ]),
  },
};
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