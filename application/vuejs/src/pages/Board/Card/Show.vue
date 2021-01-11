<template>
  <div v-if="fetchFocusedCard" class="modal" aria-labelledby="modal-title" aria-hidden="true" @click="close">
    <div class="modal-dialog" role="document" @click.prevent.stop="">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="modal-title">
            <span v-show="!isTitleEditing" @dblclick="startTitleEdit">
               {{ focusedCard.title }}
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
          <div v-if="focusedCard.content" @dblclick="startContentEdit" class="card-content">
            <p style="word-wrap: break-word"> {{ focusedCard.content }}</p>
            <table>
              <tr>
                <td>Expected effort</td>
                <td> : &nbsp;</td>
                <td>{{ focusedCard.expectedEffort }}</td>
              </tr>
              <tr>
                <td>Real effort</td>
                <td> :</td>
                <td>{{ focusedCard.realEffort }}</td>
              </tr>
              <tr>
                <td>Complete time</td>
                <td> :</td>
                <td>{{ focusedCard.completeTime }}</td>
              </tr>
              <tr>
                <td>State</td>
                <td> :</td>
                <td>{{ focusedCard.taskState }}</td>
              </tr>
            </table>
          </div>
          <p v-else @click="startContentEdit" class="empty-content">enter content.</p>
        </div>
        <div class="modal-body" v-show="isContentEditing">
          <textarea class="edit-area" v-model="editContent"></textarea>
          <table>
            <tr>
              <td>Expected effort</td>
              <td> : &nbsp;</td>
              <td><input type="text" v-model="editExpectedEffort"></td>
            </tr>
            <tr>
              <td>Real effort</td>
              <td> :</td>
              <td><input type="text" v-model="editRealEffort"></td>
            </tr>
            <tr>
              <td>Complete time</td>
              <td> :</td>
              <td>{{ editCompleteTime }}</td>
            </tr>
            <tr>
              <td>State</td>
              <td> :</td>
              <td>{{ editTaskState }}</td>
            </tr>
          </table>
        </div>
        <button type="button" class="btn btn-primary" @click="saveContent">Save</button>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-danger" @click="deleteCardAction">delete</button>
        <button type="button" class="btn btn-primary" @click="close">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import {createNamespacedHelpers} from 'vuex';

const {mapState, mapActions} = createNamespacedHelpers('board');
export default {
  name: 'CardShow',
  props: {
    cardId: {
      type: Number,
      default: null,
    },
    boardId: {
      type: Number,
      default: null,
    },
  },
  computed: {
    ...mapState(['focusedCard']),
  },
  data() {
    return {
      isContentEditing: false,
      editContent: '',
      isTitleEditing: false,
      editTitle: '',
      editExpectedEffort: '',
      editRealEffort: '',
      editCompleteTime: '',
      editTaskState: '',
    };
  },
  methods: {
    close() {
      this.$router.push({
        path: `/boards/${this.boardId}`,
        query: this.$route.query,
      });
    },
    async deleteCardAction() {
      await this.deleteCard({
        boardId: this.boardId,
        cardId: this.cardId,
      });
      window.alert('delete succeeded');
      this.close();
    },
    startContentEdit() {
      this.isContentEditing = true;
      this.editContent = this.focusedCard.content;
      this.editExpectedEffort = this.focusedCard.expectedEffort;
      this.editRealEffort = this.focusedCard.realEffort;
      this.editCompleteTime = this.focusedCard.completeTime;
      this.editTaskState = this.focusedCard.taskState;
      console.log(this.focusedCard);
    },
    startTitleEdit() {
      this.isTitleEditing = true;
      this.editTitle = this.focusedCard.title;
    },
    async saveContent() {
      this.isContentEditing = false;
      // if (this.editContent === this.focusedCard.content) return;
      await this.updateCardContent({
        boardId: this.boardId,
        cardId: this.cardId,
        content: this.editContent,
        expectedEffort: this.editExpectedEffort,
        realEffort: this.editRealEffort,
        completeTime: this.editCompleteTime,
        taskState: this.editTaskState,
      });
    },
    async saveTitle() {
      this.isTitleEditing = false;
      if (this.editTitle === this.focusedCard.title) return;
      await this.updateCardTitle({
        boardId: this.boardId,
        cardId: this.cardId,
        title: this.editTitle,
      });
    },
    ...mapActions([
      'fetchFocusedCard',
      'updateCardContent',
      'updateCardTitle',
      'deleteCard',
    ]),
  },
  watch: {
    cardId: {
      immediate: true,
      handler(cardId) {
        console.log(cardId);
        this.fetchFocusedCard({
          boardId: this.boardId,
          cardId,
        });
      },
    },
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