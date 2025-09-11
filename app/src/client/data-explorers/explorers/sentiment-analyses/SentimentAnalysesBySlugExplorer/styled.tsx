import { Flex, Td } from '@chakra-ui/react';
import styled from '@emotion/styled';

import { strokeColorByPolarity } from 'client/common/components/MultiSeriesLineGraph/constants';

const StyledFlex = styled(Flex)`
  align-items: center;
  flex-direction: column;

  & .sentiment-analyses-wrapper {
    & tbody tr {
      /* background-color: #e0e0e0; */
      /* background-color: rgb(224 224 224 / 0.5); */
      /* background-color: #939393; */
      /* background-color: #777777; */
      background-color: #6b6b6b; /* I think this one is the best? */
    }

    & tr,
    & th,
    & td {
      border-color: #ffffff;
    }

    & tr {
      border: 1px solid #ffffff;

      &:nth-of-type(odd) td {
        border-bottom-color: #ffffff;
        border-bottom-style: solid;
        border-bottom-width: 1px;
      }

      &:nth-of-type(even) td:first-child {
        /* TODO: fix this type... */
        background: ${(props) => (props.theme as any).colors?.gray?.[800]};
      }
    }

    & td {
      text-shadow: 0px 0px 4px #000000;
    }
  }
`;

const StyledTd = styled(Td)`
  &[data-polarity-key][data-polarity-value] {
    background-color: ${(props) => buildBackgroundColor(props)};
  }
`;

export { StyledFlex, StyledTd };

// *************************    UTILS    **************************************
function buildRgba(
  polKey: keyof typeof strokeColorByPolarity, // force formatting
  polValue: number,
) {
  const { rgbWeights } = strokeColorByPolarity[polKey];
  const opacity = rescaleValue({
    x: polValue,
    startRange: [-1, 1],
    endRange: [0.1, 1],
  });
  return `rgb(${rgbWeights} / ${opacity})`;
}

const keyMap = {
  compound: 'Compound',
  pos: 'Positive',
  neg: 'Negative',
  neu: 'Neutral',
};

function buildBackgroundColor(props) {
  const polarityKey = props['data-polarity-key'];

  if (polarityKey == null || polarityKey === '') {
    return 'inherit';
  }

  return buildRgba(keyMap[polarityKey], props['data-polarity-value']);
}

/**
 * @param polarityValue
 *
 * @notes generic rescale formula (aka a linear mapping)
 * ```txt
 * for mapping value `x` between range `[a,b]` to range `[c,d]`:
 *
 *            (x - a)
 * f(x) = c + ------- x (d - c)
 *            (b - a)
 *
 * code-friendly: f(x) = c + (x - a)/(b - a) * (d - c)
 * ```
 */
function rescaleValue({
  x,
  startRange = [0, 1],
  endRange = [0.5, 1],
}: {
  x: number;
  startRange: [number, number];
  endRange: [number, number];
}) {
  const [a, b] = startRange;
  const [c, d] = endRange;
  return c + ((x - a) / (b - a)) * (d - c);
}
