<template>
  <div>
    <p v-if="legend" class="questions__title --body3 --light" v-text="legend" />
    <div class="questions">
      <div
        v-for="(question, index) in questions"
        :key="question.id"
        @keydown.shift.arrow-up.prevent="
          updateQuestionAutofocus(autofocusPosition - 1)
        "
        @keydown.shift.arrow-down.prevent="
          updateQuestionAutofocus(autofocusPosition + 1)
        "
      >
        <TextAreaComponent
          v-if="question.isTextType"
          ref="text"
          :question="question"
          :isFocused="checkIfQuestionIsFocused(index)"
          @on-focus="updateQuestionAutofocus(index)"
        />

        <SingleLabelComponent
          v-if="question.isSingleLabelType"
          ref="singleLabel"
          :question="question"
          :isFocused="checkIfQuestionIsFocused(index)"
          @on-focus="updateQuestionAutofocus(index)"
          @on-user-answer="focusNext(index)"
        />

        <MultiLabelComponent
          ref="multiLabel"
          v-if="question.isMultiLabelType"
          :question="question"
          :visibleOptions="question.settings.visible_options"
          :isFocused="checkIfQuestionIsFocused(index)"
          @on-focus="updateQuestionAutofocus(index)"
        />

        <RatingComponent
          v-if="question.isRatingType"
          ref="rating"
          :question="question"
          :isFocused="checkIfQuestionIsFocused(index)"
          @on-focus="updateQuestionAutofocus(index)"
          @on-user-answer="focusNext(index)"
        />

        <RankingComponent
          v-if="question.isRankingType"
          ref="ranking"
          :question="question"
          :isFocused="checkIfQuestionIsFocused(index)"
          @on-focus="updateQuestionAutofocus(index)"
        />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuestionsComponent",
  props: {
    questions: {
      type: Array,
      required: true,
    },
    legend: {
      type: String,
    },
    autofocusPosition: {
      type: Number,
    },
  },
  computed: {
    questionsWithLoopMovement() {
      return ["singleLabel", "multiLabel", "rating", "ranking"]
        .filter((componentType) => this.$refs[componentType])
        .map((componentType) => this.$refs[componentType][0].$el);
    },
  },
  mounted() {
    this.questionsWithLoopMovement.forEach((parent) => {
      parent.addEventListener("keydown", this.handleKeyboardToMoveLoop(parent));
    });
  },
  beforeDestroy() {
    this.questionsWithLoopMovement.forEach((parent) => {
      parent.removeEventListener(
        "keydown",
        this.handleKeyboardToMoveLoop(parent)
      );
    });
  },
  methods: {
    handleKeyboardToMoveLoop(parent) {
      return (e) => {
        if (e.key !== "Tab") return;
        const isShiftKeyPressed = e.shiftKey;

        const focusable = parent.querySelectorAll(
          'input[type="checkbox"], [tabindex="0"]'
        );
        const firstElement = focusable[0];
        const lastElement = focusable[focusable.length - 1];

        const isLastElementActive = document.activeElement === lastElement;
        const isFirstElementActive = document.activeElement === firstElement;

        if (!isShiftKeyPressed && isLastElementActive) {
          this.focusOn(e, firstElement);
        } else if (isShiftKeyPressed && isFirstElementActive) {
          this.focusOn(e, lastElement);
        } else {
          const index = Array.from(focusable).findIndex(
            (r) => r === document.activeElement
          );

          const nextElementToFocus = isShiftKeyPressed
            ? focusable[index - 1]
            : focusable[index + 1];

          this.focusOn(e, nextElementToFocus);
        }
      };
    },
    focusOnFirstQuestion(e) {
      e.preventDefault();
      this.updateQuestionAutofocus(0);
    },
    focusOnLastQuestion(e) {
      e.preventDefault();
      this.updateQuestionAutofocus(this.questions.length);
    },
    focusOn($event, node) {
      $event.preventDefault();
      node.focus();
    },
    focusNext(index) {
      this.updateQuestionAutofocus(index + 1);
    },
    updateQuestionAutofocus(index) {
      this.$emit("on-focus", index);
    },
    checkIfQuestionIsFocused(index) {
      return this.autofocusPosition === index;
    },
  },
};
</script>

<style lang="scss" scoped>
.questions {
  display: flex;
  flex-direction: column;
  gap: $base-space * 4;
  &__title {
    color: $black-37;
    margin-top: 0;
    margin-bottom: $base-space * 3;
  }
}
</style>
