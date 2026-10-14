//! harmonic_compat: Pure, deterministic harmonic compatibility model over exact rationals.

use core::num::NonZeroU64;

fn gcd(mut a: u64, mut b: u64) -> u64 {
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

// ---------- Layer 0: exact arithmetic (no floats anywhere) ----------

/// INVARIANT: gcd(num, den) == 1. Reduced form is the unique representation,
/// so encoding is canonical by construction.
#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Ratio {
    num: NonZeroU64,
    den: NonZeroU64,
}

#[derive(Debug, PartialEq, Eq, Clone, Copy)]
pub enum RatioError {
    ZeroTerm,
    Overflow,
}

impl Ratio {
    pub fn new(num: u64, den: u64) -> Result<Ratio, RatioError> {
        if num == 0 || den == 0 {
            return Err(RatioError::ZeroTerm);
        }
        let g = gcd(num, den);
        let n = num / g;
        let d = den / g;
        Ok(Ratio {
            num: NonZeroU64::new(n).ok_or(RatioError::ZeroTerm)?,
            den: NonZeroU64::new(d).ok_or(RatioError::ZeroTerm)?,
        })
    }

    pub fn mul(self, rhs: Ratio) -> Result<Ratio, RatioError> {
        let g1 = gcd(self.num.get(), rhs.den.get());
        let g2 = gcd(rhs.num.get(), self.den.get());

        let n1 = self.num.get() / g1;
        let d2 = rhs.den.get() / g1;
        let n2 = rhs.num.get() / g2;
        let d1 = self.den.get() / g2;

        let new_num = n1.checked_mul(n2).ok_or(RatioError::Overflow)?;
        let new_den = d1.checked_mul(d2).ok_or(RatioError::Overflow)?;

        Ok(Ratio {
            num: NonZeroU64::new(new_num).ok_or(RatioError::ZeroTerm)?,
            den: NonZeroU64::new(new_den).ok_or(RatioError::ZeroTerm)?,
        })
    }

    pub fn inv(self) -> Ratio {
        Ratio {
            num: self.den,
            den: self.num,
        }
    }

    pub fn num(&self) -> u64 {
        self.num.get()
    }

    pub fn den(&self) -> u64 {
        self.den.get()
    }

    /// Tenney height: num * den. Complexity measure for the ratio.
    pub fn height(&self) -> u128 {
        (self.num.get() as u128) * (self.den.get() as u128)
    }
}

// ---------- Layer 1: octave equivalence ----------

/// Fold into [1, 2); returns (class representative, octave shift applied).
/// Law: octave_class(r * 2^k).0 == octave_class(r).0 for all k.
pub fn octave_class(r: Ratio) -> Result<(Ratio, i32), RatioError> {
    let mut num = r.num();
    let mut den = r.den();
    let mut k: i32 = 0;

    while num < den {
        if den % 2 == 0 {
            den /= 2;
        } else {
            num = num.checked_mul(2).ok_or(RatioError::Overflow)?;
        }
        k = k.checked_add(1).ok_or(RatioError::Overflow)?;
    }

    while den.checked_mul(2).map_or(false, |two_den| num >= two_den) {
        if num % 2 == 0 {
            num /= 2;
        } else {
            den = den.checked_mul(2).ok_or(RatioError::Overflow)?;
        }
        k = k.checked_sub(1).ok_or(RatioError::Overflow)?;
    }

    let class_ratio = Ratio::new(num, den)?;
    Ok((class_ratio, k))
}

// ---------- Layer 2: relation + policy ----------

/// Without a bound, any two rationals are commensurate (common fundamental
/// always exists), so "compatible" would be vacuous. The bound IS the model.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct Policy {
    pub max_height: u128,
    pub octave_equivalence: bool,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Relation {
    Unison,
    OctaveEquivalent { octaves: i32 },
    /// a : b == lo : hi, reduced, height(lo/hi) <= policy.max_height
    Harmonic { lo: NonZeroU64, hi: NonZeroU64 },
    /// Related only above the policy bound.
    Incommensurate,
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash)]
pub struct Tone(pub Ratio); // dimensionless; reference frame is caller's concern

pub trait Resonance {
    fn relate(&self, other: &Self, policy: &Policy) -> Result<Relation, RatioError>;
    fn compatible(&self, other: &Self, policy: &Policy) -> Result<bool, RatioError>;
}

impl Resonance for Tone {
    fn relate(&self, other: &Self, policy: &Policy) -> Result<Relation, RatioError> {
        if self == other {
            return Ok(Relation::Unison);
        }

        let r_diff = other.0.mul(self.0.inv())?;

        if policy.octave_equivalence {
            let (class_ratio, k) = octave_class(r_diff)?;
            let one = Ratio::new(1, 1)?;
            if class_ratio == one {
                let octaves = -k;
                return Ok(Relation::OctaveEquivalent { octaves });
            }

            let r_diff_inv = self.0.mul(other.0.inv())?;
            let (class_ratio_inv, _) = octave_class(r_diff_inv)?;

            let (best_class, lo, hi) = if class_ratio.height() <= class_ratio_inv.height() {
                (class_ratio, class_ratio.den(), class_ratio.num())
            } else {
                (class_ratio_inv, class_ratio_inv.den(), class_ratio_inv.num())
            };

            let height = best_class.height();
            if height <= policy.max_height {
                Ok(Relation::Harmonic {
                    lo: NonZeroU64::new(lo).ok_or(RatioError::ZeroTerm)?,
                    hi: NonZeroU64::new(hi).ok_or(RatioError::ZeroTerm)?,
                })
            } else {
                Ok(Relation::Incommensurate)
            }
        } else {
            let num = r_diff.num();
            let den = r_diff.den();
            let lo = core::cmp::min(num, den);
            let hi = core::cmp::max(num, den);
            let height = r_diff.height();

            if height <= policy.max_height {
                Ok(Relation::Harmonic {
                    lo: NonZeroU64::new(lo).ok_or(RatioError::ZeroTerm)?,
                    hi: NonZeroU64::new(hi).ok_or(RatioError::ZeroTerm)?,
                })
            } else {
                Ok(Relation::Incommensurate)
            }
        }
    }

    fn compatible(&self, other: &Self, policy: &Policy) -> Result<bool, RatioError> {
        let rel = self.relate(other, policy)?;
        Ok(match rel {
            Relation::Unison | Relation::OctaveEquivalent { .. } | Relation::Harmonic { .. } => true,
            Relation::Incommensurate => false,
        })
    }
}

// ---------- Layer 3: Referent & Assignment ----------

/// Represents an architectural component, message schema, or capability tier
/// that participates in the harmonic compatibility network.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct ComponentRef {
    pub namespace_id: u32,
    pub schema_version: (u16, u16, u16), // semver: major, minor, patch
    pub structural_complexity: u64,     // e.g., field count or AST node weight
}

pub trait TonalAssignment {
    /// Deterministically map a component reference to a dimensionless Tone.
    /// Ensures that the ratio components derive strictly from structural metrics.
    fn assign_tone(&self) -> Result<Tone, RatioError>;
}

impl TonalAssignment for ComponentRef {
    fn assign_tone(&self) -> Result<Tone, RatioError> {
        let num_val = core::cmp::max(1, self.schema_version.0 as u64);
        let den_val = core::cmp::max(1, self.structural_complexity);

        let ratio = Ratio::new(num_val, den_val)?;
        Ok(Tone(ratio))
    }
}

// ---------- Referent: closed label set ----------

#[derive(Clone, Copy, Debug, PartialEq, Eq, Hash, PartialOrd, Ord)]
pub enum Noble8 {
    Au,
    Pt,
    Ir,
    Rh,
    Ru,
    Ag,
    Pd,
    Os,
}

impl Noble8 {
    pub const ALL: [Noble8; 8] = [
        Noble8::Au,
        Noble8::Pt,
        Noble8::Ir,
        Noble8::Rh,
        Noble8::Ru,
        Noble8::Ag,
        Noble8::Pd,
        Noble8::Os,
    ];

    /// Reference data only (79, 78, 77, 45, 44, 47, 46, 76); not an input to tuning.
    pub fn atomic_number(self) -> u8 {
        match self {
            Noble8::Au => 79,
            Noble8::Pt => 78,
            Noble8::Ir => 77,
            Noble8::Rh => 45,
            Noble8::Ru => 44,
            Noble8::Ag => 47,
            Noble8::Pd => 46,
            Noble8::Os => 76,
        }
    }

    pub fn symbol(self) -> &'static str {
        match self {
            Noble8::Au => "Au",
            Noble8::Pt => "Pt",
            Noble8::Ir => "Ir",
            Noble8::Rh => "Rh",
            Noble8::Ru => "Ru",
            Noble8::Ag => "Ag",
            Noble8::Pd => "Pd",
            Noble8::Os => "Os",
        }
    }
}

// ---------- Assignment: the declared mapping ----------

#[derive(Debug, PartialEq, Eq)]
pub enum AssignError {
    MissingLabel(Noble8),
    DuplicateLabel(Noble8),
    /// Two labels map to tones that relate as Unison or OctaveEquivalent
    /// under the supplied policy, so they would be indistinguishable.
    Indistinct(Noble8, Noble8),
    Ratio(RatioError),
}

impl From<RatioError> for AssignError {
    fn from(err: RatioError) -> Self {
        AssignError::Ratio(err)
    }
}

/// INVARIANT: total over Noble8, and pairwise distinct under `policy`.
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Assignment {
    tones: [Tone; 8],
    policy: Policy,
}

impl Assignment {
    pub fn new(entries: &[(Noble8, Tone)], policy: Policy) -> Result<Assignment, AssignError> {
        let mut seen = [false; 8];
        let mut tones = [None; 8];

        for &(label, tone) in entries {
            let idx = label as usize;
            if seen[idx] {
                return Err(AssignError::DuplicateLabel(label));
            }
            seen[idx] = true;
            tones[idx] = Some(tone);
        }

        for &label in &Noble8::ALL {
            if tones[label as usize].is_none() {
                return Err(AssignError::MissingLabel(label));
            }
        }

        let array_tones: [Tone; 8] = [
            tones[0].unwrap(),
            tones[1].unwrap(),
            tones[2].unwrap(),
            tones[3].unwrap(),
            tones[4].unwrap(),
            tones[5].unwrap(),
            tones[6].unwrap(),
            tones[7].unwrap(),
        ];

        for i in 0..8 {
            for j in (i + 1)..8 {
                let rel = array_tones[i].relate(&array_tones[j], &policy)?;
                match rel {
                    Relation::Unison | Relation::OctaveEquivalent { .. } => {
                        return Err(AssignError::Indistinct(Noble8::ALL[i], Noble8::ALL[j]));
                    }
                    Relation::Harmonic { .. } | Relation::Incommensurate => {}
                }
            }
        }

        Ok(Assignment {
            tones: array_tones,
            policy,
        })
    }

    pub fn tone(&self, label: Noble8) -> Tone {
        self.tones[label as usize]
    }

    pub fn policy(&self) -> &Policy {
        &self.policy
    }

    /// Full 8x8 relation matrix; row-major in Noble8::ALL order.
    pub fn matrix(&self) -> Result<[[Relation; 8]; 8], RatioError> {
        let mut mat = [[Relation::Unison; 8]; 8];
        for i in 0..8 {
            for j in 0..8 {
                mat[i][j] = self.tones[i].relate(&self.tones[j], &self.policy)?;
            }
        }
        Ok(mat)
    }
}

// ---------- Laws (property-test signatures & verification tests) ----------

#[cfg(test)]
mod assignment_laws {
    use super::*;

    fn total(a: &Assignment) {
        for &label in &Noble8::ALL {
            let _ = a.tone(label);
        }
    }

    fn injective(a: &Assignment) {
        let p = a.policy();
        for i in 0..8 {
            for j in (i + 1)..8 {
                let t1 = a.tone(Noble8::ALL[i]);
                let t2 = a.tone(Noble8::ALL[j]);
                let rel = t1.relate(&t2, p).unwrap();
                assert!(
                    !matches!(rel, Relation::Unison | Relation::OctaveEquivalent { .. }),
                    "Injective law failed for {:?} and {:?}",
                    Noble8::ALL[i],
                    Noble8::ALL[j]
                );
            }
        }
    }

    fn matrix_symmetric(a: &Assignment) {
        let mat = a.matrix().unwrap();
        for i in 0..8 {
            for j in 0..8 {
                match (mat[i][j], mat[j][i]) {
                    (Relation::Unison, Relation::Unison) => {}
                    (
                        Relation::OctaveEquivalent { octaves: k1 },
                        Relation::OctaveEquivalent { octaves: k2 },
                    ) => {
                        assert_eq!(k1, -k2);
                    }
                    (
                        Relation::Harmonic { lo: l1, hi: h1 },
                        Relation::Harmonic { lo: l2, hi: h2 },
                    ) => {
                        assert_eq!(l1, l2);
                        assert_eq!(h1, h2);
                    }
                    (Relation::Incommensurate, Relation::Incommensurate) => {}
                    _ => panic!(
                        "Matrix symmetry violated between {:?} and {:?}",
                        Noble8::ALL[i],
                        Noble8::ALL[j]
                    ),
                }
            }
        }
    }

    fn diagonal_unison(a: &Assignment) {
        let mat = a.matrix().unwrap();
        for i in 0..8 {
            assert_eq!(mat[i][i], Relation::Unison);
        }
    }

    #[test]
    fn test_assignment_valid() {
        let policy = Policy {
            max_height: 100,
            octave_equivalence: true,
        };
        let ratios = [
            (1, 1),
            (9, 8),
            (5, 4),
            (4, 3),
            (3, 2),
            (5, 3),
            (15, 8),
            (16, 9),
        ];
        let entries: Vec<(Noble8, Tone)> = Noble8::ALL
            .iter()
            .zip(ratios.iter())
            .map(|(&label, &(n, d))| (label, Tone(Ratio::new(n, d).unwrap())))
            .collect();

        let assignment = Assignment::new(&entries, policy).unwrap();

        total(&assignment);
        injective(&assignment);
        matrix_symmetric(&assignment);
        diagonal_unison(&assignment);
    }

    #[test]
    fn test_assignment_errors() {
        let policy = Policy {
            max_height: 100,
            octave_equivalence: true,
        };
        let t1 = Tone(Ratio::new(1, 1).unwrap());
        let t2 = Tone(Ratio::new(9, 8).unwrap());

        // Duplicate error
        let dup_entries = vec![(Noble8::Au, t1), (Noble8::Au, t2)];
        assert_eq!(
            Assignment::new(&dup_entries, policy),
            Err(AssignError::DuplicateLabel(Noble8::Au))
        );

        // Missing error
        let miss_entries = vec![(Noble8::Au, t1)];
        assert_eq!(
            Assignment::new(&miss_entries, policy),
            Err(AssignError::MissingLabel(Noble8::Pt))
        );

        // Indistinct error (Unison)
        let ratios = [(1, 1); 8];
        let indistinct_entries: Vec<(Noble8, Tone)> = Noble8::ALL
            .iter()
            .zip(ratios.iter())
            .map(|(&label, &(n, d))| (label, Tone(Ratio::new(n, d).unwrap())))
            .collect();
        assert_eq!(
            Assignment::new(&indistinct_entries, policy),
            Err(AssignError::Indistinct(Noble8::Au, Noble8::Pt))
        );

        // Indistinct error (OctaveEquivalent)
        let mut oct_ratios = [(1, 1); 8];
        oct_ratios[1] = (2, 1);
        let oct_entries: Vec<(Noble8, Tone)> = Noble8::ALL
            .iter()
            .zip(oct_ratios.iter())
            .map(|(&label, &(n, d))| (label, Tone(Ratio::new(n, d).unwrap())))
            .collect();
        assert_eq!(
            Assignment::new(&oct_entries, policy),
            Err(AssignError::Indistinct(Noble8::Au, Noble8::Pt))
        );
    }

    #[test]
    fn test_noble8_methods() {
        assert_eq!(Noble8::Au.atomic_number(), 79);
        assert_eq!(Noble8::Au.symbol(), "Au");
        assert_eq!(Noble8::Pt.atomic_number(), 78);
        assert_eq!(Noble8::Pt.symbol(), "Pt");
        assert_eq!(Noble8::Ir.atomic_number(), 77);
        assert_eq!(Noble8::Ir.symbol(), "Ir");
        assert_eq!(Noble8::Rh.atomic_number(), 45);
        assert_eq!(Noble8::Rh.symbol(), "Rh");
        assert_eq!(Noble8::Ru.atomic_number(), 44);
        assert_eq!(Noble8::Ru.symbol(), "Ru");
        assert_eq!(Noble8::Ag.atomic_number(), 47);
        assert_eq!(Noble8::Ag.symbol(), "Ag");
        assert_eq!(Noble8::Pd.atomic_number(), 46);
        assert_eq!(Noble8::Pd.symbol(), "Pd");
        assert_eq!(Noble8::Os.atomic_number(), 76);
        assert_eq!(Noble8::Os.symbol(), "Os");
    }
}

#[cfg(test)]
mod laws {
    use super::*;

    #[test]
    fn test_reflexive_law() {
        let policy = Policy {
            max_height: 100,
            octave_equivalence: true,
        };
        let tones = [
            Tone(Ratio::new(1, 1).unwrap()),
            Tone(Ratio::new(3, 2).unwrap()),
            Tone(Ratio::new(440, 1).unwrap()),
            Tone(Ratio::new(17, 19).unwrap()),
        ];

        for tone in tones {
            reflexive(tone, policy);
        }
    }

    fn reflexive(t: Tone, p: Policy) {
        let rel = t.relate(&t, &p).unwrap();
        assert_eq!(rel, Relation::Unison);
        assert!(t.compatible(&t, &p).unwrap());
    }

    #[test]
    fn test_symmetric_law() {
        let policy = Policy {
            max_height: 100,
            octave_equivalence: true,
        };
        let pairs = [
            (
                Tone(Ratio::new(1, 1).unwrap()),
                Tone(Ratio::new(2, 1).unwrap()),
            ),
            (
                Tone(Ratio::new(3, 2).unwrap()),
                Tone(Ratio::new(4, 3).unwrap()),
            ),
            (
                Tone(Ratio::new(5, 4).unwrap()),
                Tone(Ratio::new(15, 8).unwrap()),
            ),
        ];

        for (a, b) in pairs {
            symmetric(a, b, policy);
        }
    }

    fn symmetric(a: Tone, b: Tone, p: Policy) {
        let rel_ab = a.relate(&b, &p).unwrap();
        let rel_ba = b.relate(&a, &p).unwrap();

        match (rel_ab, rel_ba) {
            (Relation::Unison, Relation::Unison) => {}
            (
                Relation::OctaveEquivalent { octaves: k1 },
                Relation::OctaveEquivalent { octaves: k2 },
            ) => {
                assert_eq!(k1, -k2);
            }
            (
                Relation::Harmonic { lo: l1, hi: h1 },
                Relation::Harmonic { lo: l2, hi: h2 },
            ) => {
                assert_eq!(l1, l2);
                assert_eq!(h1, h2);
            }
            (Relation::Incommensurate, Relation::Incommensurate) => {}
            _ => panic!("Symmetry violated between {:?} and {:?}", a, b),
        }

        assert_eq!(
            a.compatible(&b, &p).unwrap(),
            b.compatible(&a, &p).unwrap()
        );
    }

    #[test]
    fn test_octave_invariant_law() {
        let policy = Policy {
            max_height: 100,
            octave_equivalence: true,
        };
        let a = Tone(Ratio::new(3, 2).unwrap());
        let b = Tone(Ratio::new(5, 4).unwrap());

        for k in -5..=5 {
            octave_invariant(a, b, k, policy);
        }
    }

    fn octave_invariant(a: Tone, b: Tone, k: i32, p: Policy) {
        if !p.octave_equivalence {
            return;
        }
        let (a_class, _) = octave_class(a.0).unwrap();
        let (b_class, _) = octave_class(b.0).unwrap();

        let mut b_shifted_num = b.0.num();
        let mut b_shifted_den = b.0.den();
        if k >= 0 {
            for _ in 0..k {
                b_shifted_num = b_shifted_num.checked_mul(2).unwrap();
            }
        } else {
            for _ in 0..(-k) {
                b_shifted_den = b_shifted_den.checked_mul(2).unwrap();
            }
        }
        let b_shifted = Tone(Ratio::new(b_shifted_num, b_shifted_den).unwrap());

        let (b_shifted_class, _) = octave_class(b_shifted.0).unwrap();
        assert_eq!(b_class, b_shifted_class);

        let rel_orig = Tone(a_class).relate(&Tone(b_class), &p).unwrap();
        let rel_shifted = a.relate(&b_shifted, &p).unwrap();

        match (rel_orig, rel_shifted) {
            (Relation::Harmonic { lo: l1, hi: h1 }, Relation::Harmonic { lo: l2, hi: h2 }) => {
                assert_eq!(l1, l2);
                assert_eq!(h1, h2);
            }
            (Relation::Unison, Relation::Unison)
            | (Relation::Unison, Relation::OctaveEquivalent { .. })
            | (Relation::OctaveEquivalent { .. }, Relation::OctaveEquivalent { .. })
            | (Relation::Incommensurate, Relation::Incommensurate) => {}
            _ => panic!("Octave invariance failed for k={}", k),
        }
    }

    #[test]
    fn test_monotone_in_bound_law() {
        let p1 = Policy {
            max_height: 10,
            octave_equivalence: true,
        };
        let p2 = Policy {
            max_height: 100,
            octave_equivalence: true,
        };
        let a = Tone(Ratio::new(3, 2).unwrap());
        let b = Tone(Ratio::new(5, 4).unwrap());

        monotone_in_bound(a, b, p1, p2);
    }

    fn monotone_in_bound(a: Tone, b: Tone, p1: Policy, p2: Policy) {
        assert!(p1.max_height <= p2.max_height);
        assert_eq!(p1.octave_equivalence, p2.octave_equivalence);

        if a.compatible(&b, &p1).unwrap() {
            assert!(a.compatible(&b, &p2).unwrap());
        }
    }

    #[test]
    fn test_deterministic_law() {
        let policy = Policy {
            max_height: 50,
            octave_equivalence: true,
        };
        let a = Tone(Ratio::new(7, 5).unwrap());
        let b = Tone(Ratio::new(9, 8).unwrap());

        deterministic(a, b, policy);
    }

    fn deterministic(a: Tone, b: Tone, p: Policy) {
        let res1 = a.relate(&b, &p).unwrap();
        let res2 = a.relate(&b, &p).unwrap();
        let res3 = a.relate(&b, &p).unwrap();

        assert_eq!(res1, res2);
        assert_eq!(res2, res3);
    }

    #[test]
    fn test_non_transitivity_counterexample() {
        // Demonstrate that Compatible(a,b) and Compatible(b,c) does not imply Compatible(a,c).
        let policy = Policy {
            max_height: 10,
            octave_equivalence: false,
        };

        // Ratio(1, 1) to Ratio(3, 2): diff = 3/2, height = 6 <= 10 -> Compatible!
        let a = Tone(Ratio::new(1, 1).unwrap());
        let b = Tone(Ratio::new(3, 2).unwrap());

        // Ratio(3, 2) to Ratio(9, 4): diff = 3/2, height = 6 <= 10 -> Compatible!
        let c = Tone(Ratio::new(9, 4).unwrap());

        assert!(a.compatible(&b, &policy).unwrap());
        assert!(b.compatible(&c, &policy).unwrap());

        // Ratio(1, 1) to Ratio(9, 4): diff = 9/4, height = 36 > 10 -> Incommensurate (Not Compatible!)
        assert!(!a.compatible(&c, &policy).unwrap());
    }

    #[test]
    fn test_referent_tonal_assignment() {
        let comp1 = ComponentRef {
            namespace_id: 1,
            schema_version: (3, 0, 0),
            structural_complexity: 2,
        };
        let tone1 = comp1.assign_tone().unwrap();
        assert_eq!(tone1.0, Ratio::new(3, 2).unwrap());

        let comp2 = ComponentRef {
            namespace_id: 1,
            schema_version: (1, 0, 0),
            structural_complexity: 1,
        };
        let tone2 = comp2.assign_tone().unwrap();
        assert_eq!(tone2.0, Ratio::new(1, 1).unwrap());

        let policy = Policy {
            max_height: 10,
            octave_equivalence: true,
        };
        assert!(tone1.compatible(&tone2, &policy).unwrap());
    }
}
