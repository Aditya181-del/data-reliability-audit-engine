import { useState } from 'react';
import { Zone2Explanation as Zone2Data, Audience } from './types';

import { AudienceSelector } from './AudienceSelector';
import { SummaryCard } from './SummaryCard';
import { KeyFindingsList } from './KeyFindingsList';
import { DecisionRationale } from './DecisionRationale';
import { NextSteps } from './NextSteps';
import { TransparencyPanel } from './TransparencyPanel';

interface Props {
  explanation: Zone2Data;
  onAudienceChange: (audience: Audience) => void;
  rawAudit: unknown; // passed only to TransparencyPanel
}

export const Zone2Explanation: React.FC<Props> = ({
  explanation,
  onAudienceChange,
  rawAudit,
}) => {
  return (
    <section className="space-y-16">
      <AudienceSelector
        value={explanation.audience}
        onChange={onAudienceChange}
      />

      <SummaryCard text={explanation.summary} />

      <KeyFindingsList findings={explanation.key_findings} />

      <DecisionRationale text={explanation.decision_rationale} />

      <NextSteps steps={explanation.next_steps} />

      <TransparencyPanel audit={rawAudit} />
    </section>
  );
};
