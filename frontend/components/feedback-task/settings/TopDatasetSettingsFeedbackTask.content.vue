<template>
  <div class="top-content" :class="separator ? '--separator' : null">
    <h1>Dataset settings</h1>
    <base-button
      :to="{ name: 'dataset-id-annotation-mode', params: { id: datasetId } }"
      class="secondary text"
    >
      <svgicon name="chevron-left" width="10" height="10" color="#4C4EA3" />
      See your dataset
    </base-button>
  </div>
</template>

<script>
export default {
  name: "TopDatasetSettingsFeedbackTaskContent",
  props: {
    datasetId: {
      type: String,
      required: true,
    },
    separator: {
      type: Boolean,
      default: true,
    },
  },
};
</script>

<style lang="scss" scoped>
.top-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2em;
  &.--separator {
    padding-bottom: 2em;
    border-bottom: 1px solid #e6e6e6;
  }
}
</style>
