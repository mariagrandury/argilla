<template>
  <div
    v-if="text"
    ref="tooltipWrapper"
    class="tooltip"
    @mouseenter="show"
    @mouseleave="hide"
  >
    <slot></slot>

    <div
      ref="tooltipText"
      :class="[
        'tooltip-content',
        positionClass,
        showTooltip ? 'tooltip-content--show' : 'tooltip-content--hide',
      ]"
      :style="{
        top: tooltipPosition.top + 'px',
        left: tooltipPosition.left + 'px',
      }"
      v-text="text"
    />
  </div>
</template>

<script>
export default {
  data() {
    return {
      showTooltip: false,
      tooltipPosition: {
        top: 0,
        left: 0,
      },
    };
  },
  props: {
    text: {
      type: String,
      required: true,
    },
    position: {
      type: String,
      default: "top",
    },
    offset: {
      type: Number,
      default: 8,
    },
  },
  methods: {
    show() {
      this.showTooltip = true;
      this.calculateTooltipPosition();
    },
    hide() {
      this.showTooltip = false;
    },
    calculateTooltipPosition() {
      const tooltipWrapper = this.$refs.tooltipWrapper;
      const tooltipText = this.$refs.tooltipText;
      const tooltipRect = tooltipWrapper.getBoundingClientRect();
      const tooltipTextRect = tooltipText.getBoundingClientRect();

      switch (this.position) {
        case "top":
          this.tooltipPosition = {
            top: tooltipRect.top - tooltipTextRect.height - this.offset,
            left:
              tooltipRect.left +
              tooltipRect.width / 2 -
              tooltipTextRect.width / 2,
          };
          break;
        case "bottom":
          this.tooltipPosition = {
            top: tooltipRect.top - tooltipRect.height + tooltipTextRect.height,
            left:
              tooltipRect.left +
              tooltipRect.width / 2 -
              tooltipTextRect.width / 2,
          };
          break;
        case "left":
          this.tooltipPosition = {
            top:
              tooltipRect.top +
              tooltipRect.height / 2 -
              tooltipTextRect.height / 2,
            left: tooltipRect.left - tooltipTextRect.width - this.offset,
          };
          break;
        case "right":
          this.tooltipPosition = {
            top:
              tooltipRect.top +
              tooltipRect.height / 2 -
              tooltipTextRect.height / 2,
            left: tooltipRect.right + this.offset,
          };
          break;
        default:
          break;
      }
    },
  },
  computed: {
    positionClass() {
      return `position-${this.position}`;
    },
  },
};
</script>

<style scoped lang="scss">
.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip-content {
  position: fixed;
  margin: auto;
  overflow-wrap: break-word;
  pointer-events: none;
  z-index: 2;
  white-space: nowrap;
  padding: 6px $base-space;
  transform: none;
  background: $tooltip-bg;
  color: $tooltip-color;
  border-radius: $tooltip-border-radius;
  @include font-size($tooltip-font-size);
  font-weight: 500;
  white-space: pre;
  &--hide {
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.2s ease-in-out;
  }
  &--show {
    opacity: 1;
    transition: opacity 0.2s ease-in-out 0.2s;
  }
}

.tooltip-content {
  &.position-top {
    &::after {
      content: "";
      position: absolute;
      top: 100%;
      left: 50%;
      transform: translateX(-50%);
      border-width: 5px;
      border-style: solid;
      border-color: $tooltip-bg transparent transparent transparent;
    }
  }
  &.position-bottom {
    &::after {
      content: "";
      position: absolute;
      bottom: 100%;
      left: 50%;
      transform: translateX(-50%);
      border-width: 5px;
      border-style: solid;
      border-color: transparent transparent $tooltip-bg transparent;
    }
  }
  &.position-left {
    &::after {
      content: "";
      position: absolute;
      bottom: 50%;
      left: 100%;
      transform: translateY(50%);
      border-width: 5px;
      border-style: solid;
      border-color: transparent transparent transparent $tooltip-bg;
    }
  }
  &.position-right {
    &::after {
      content: "";
      position: absolute;
      bottom: 50%;
      right: 100%;
      transform: translateY(50%);
      border-width: 5px;
      border-style: solid;
      border-color: transparent $tooltip-bg transparent transparent;
    }
  }
}
</style>
