<template>
  <div class="board">
    <MenuBar></MenuBar>
    <BoardArea></BoardArea>
  </div>
</template>

<script>
import MenuBar from './components/MenuBar';
import BoardArea from './components/BoardArea'

export default {
  name: 'Board',
  components: {
    BoardArea,
    MenuBar
  },
};
</script>
<style lang="scss" scoped>
</style>