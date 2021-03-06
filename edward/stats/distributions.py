from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf

from edward.util import get_dims
from itertools import product
from scipy import stats

distributions = tf.contrib.distributions


class Distribution(object):
  """A light wrapper to directly call methods from
  `tf.contrib.distributions` in SciPy style.

  Examples
  --------
  >>> norm.logpdf(tf.constant(0.0))
  >>> bernoulli.logpmf(tf.constant([0.0, 1.0]), p=tf.constant([0.5, 0.4]))
  """
  def __init__(self, dist):
    self._dist = dist

  def batch_shape(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.batch_shape()

  def get_batch_shape(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.get_batch_shape()

  def event_shape(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.event_shape()

  def get_event_shape(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.get_event_shape()

  def sample(self, sample_shape=(), seed=None, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.sample(sample_shape, seed)

  def sample_n(self, n, seed=None, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.sample_n(n, seed)

  def log_prob(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.log_prob(value)

  def prob(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.prob(value)

  def log_cdf(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.log_cdf(value)

  def cdf(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.cdf(value)

  def entropy(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.entropy()

  def mean(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.mean()

  def variance(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.variance()

  def std(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.std()

  def mode(self, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.mode()

  def log_pdf(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.log_pdf(value)

  def pdf(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.pdf(value)

  def log_pmf(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.log_pmf(value)

  def pmf(self, value, *args, **kwargs):
    rv = self._dist(*args, **kwargs)
    return rv.pmf(value)

  def rvs(self, *args, **kwargs):
    """Returns samples as a NumPy array. Unlike the other methods,
    this method follows the arguments of SciPy.
    """
    raise NotImplementedError()

  def logpdf(self, value, *args, **kwargs):
    """Backwards compatibility with SciPy."""
    rv = self._dist(*args, **kwargs)
    return rv.log_pdf(value)

  def logpmf(self, value, *args, **kwargs):
    """Backwards compatibility with SciPy."""
    rv = self._dist(*args, **kwargs)
    return rv.log_pmf(value)


class Bernoulli(Distribution):
  """Bernoulli distribution.
  """
  def __init__(self):
    super(Bernoulli, self).__init__(distributions.Bernoulli)

  def rvs(self, p, size=1):
    """Random variates.

    Parameters
    ----------
    p : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`p\in(0,1)`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.

    Examples
    --------
    >>> x = bernoulli.rvs(p=0.5, size=1)
    >>> print(x.shape)
    (1,)
    >>> x = bernoulli.rvs(p=np.array([0.5]), size=1)
    >>> print(x.shape)
    (1, 1)
    >>> x = bernoulli.rvs(p=np.array([0.5, 0.2]), size=3)
    >>> print(x.shape)
    (3, 2)
    """
    if not isinstance(p, np.ndarray):
      p = np.asarray(p)
    if len(p.shape) == 0:
      return stats.bernoulli.rvs(p, size=size)

    x = []
    for pidx in np.nditer(p):
      x += [stats.bernoulli.rvs(pidx, size=size)]

    x = np.asarray(x).transpose()
    return x


class Beta(Distribution):
  """Beta distribution.
  """
  def __init__(self):
    super(Beta, self).__init__(distributions.Beta)

  def rvs(self, a, b, size=1):
    """Random variates.

    Parameters
    ----------
    a : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`a > 0`.
    b : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`b > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(a, np.ndarray):
      a = np.asarray(a)
    if not isinstance(b, np.ndarray):
      b = np.asarray(b)
    if len(a.shape) == 0:
      return stats.beta.rvs(a, b, size=size)

    x = []
    for aidx, bidx in zip(np.nditer(a), np.nditer(b)):
      x += [stats.beta.rvs(aidx, bidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x


class Binom(Distribution):
  """Binomial distribution.
  """
  def __init__(self):
    super(Binom, self).__init__(None)

  def rvs(self, n, p, size=1):
    """Random variates.

    Parameters
    ----------
    n : int or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`n > 0`.
    p : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`p\in(0,1)`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(n, np.ndarray):
      n = np.asarray(n)
    if not isinstance(p, np.ndarray):
      p = np.asarray(p)
    if len(n.shape) == 0:
      return stats.binom.rvs(n, p, size=size)

    x = []
    for nidx, pidx in zip(np.nditer(n), np.nditer(p)):
      x += [stats.binom.rvs(nidx, pidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpmf(self, x, n, p):
    """Log of the probability density function.
    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    n : int
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`n > 0`.
    p : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`p\in(0,1)`.
    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    x = tf.cast(x, dtype=tf.float32)
    n = tf.cast(n, dtype=tf.float32)
    p = tf.cast(p, dtype=tf.float32)
    return tf.lgamma(n + 1.0) - tf.lgamma(x + 1.0) - tf.lgamma(n - x + 1.0) + \
        x * tf.log(p) + (n - x) * tf.log(1.0 - p)


class Categorical(Distribution):
  """Categorical distribution.
  """
  def __init__(self):
    super(Categorical, self).__init__(distributions.Categorical)


class Chi2(Distribution):
  """:math:`\chi^2` distribution.
  """
  def __init__(self):
    super(Chi2, self).__init__(None)

  def rvs(self, df, size=1):
    """Random variates.

    Parameters
    ----------
    df : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`df > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(df, np.ndarray):
      df = np.asarray(df)
    if len(df.shape) == 0:
      return stats.chi2.rvs(df, size=size)

    x = []
    for dfidx in np.nditer(df):
      x += [stats.chi2.rvs(dfidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpdf(self, x, df):
    """Log of the probability density function.
    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    df : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`df > 0`.
    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    x = tf.cast(x, dtype=tf.float32)
    df = tf.cast(df, dtype=tf.float32)
    return (0.5 * df - 1) * tf.log(x) - 0.5 * x - \
        0.5 * df * tf.log(2.0) - tf.lgamma(0.5 * df)


class Dirichlet(Distribution):
  """Dirichlet distribution.
  """
  def __init__(self):
    super(Dirichlet, self).__init__(distributions.Dirichlet)

  def rvs(self, alpha, size=1):
    """Random variates.

    Parameters
    ----------
    alpha : np.ndarray
      1-D or 2-D tensor, with each :math:`\\alpha` constrained
      to :math:`\\alpha_i > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if len(alpha.shape) == 1:
      # stats.dirichlet.rvs defaults to (size x alpha.shape)
      return stats.dirichlet.rvs(alpha, size=size)

    x = []
    # This doesn't work for non-matrix parameters.
    for alpharow in alpha:
      x += [stats.dirichlet.rvs(alpharow, size=size)]

    # This only works for rank 3 tensor.
    x = np.rollaxis(np.asarray(x), 1)
    return x


class DirichletMultinomial(Distribution):
  """Dirichlet-Multinomial distribution.
  """
  def __init__(self):
    super(DirichletMultinomial, self).__init__(
        distributions.DirichletMultinomial)


class Exponential(Distribution):
  """Exponential distribution.
  """
  def __init__(self):
    super(Exponential, self).__init__(distributions.Exponential)

  def rvs(self, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    scale : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(scale.shape) == 0:
      return stats.expon.rvs(scale=scale, size=size)

    x = []
    for scaleidx in np.nditer(scale):
      x += [stats.expon.rvs(scale=scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x


class Gamma(Distribution):
  """Gamma distribution.

  Shape/scale parameterization (typically denoted: :math:`(k, \\theta)`)
  """
  def __init__(self):
    super(Gamma, self).__init__(distributions.Gamma)

  def rvs(self, a, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    a : float or np.ndarray
      **Shape** parameter. 0-D or 1-D tensor, with all elements
      constrained to :math:`a > 0`.
    scale : float or np.ndarray
      **Scale** parameter. 0-D or 1-D tensor, with all elements
      constrained to :math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(a, np.ndarray):
      a = np.asarray(a)
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(a.shape) == 0:
      return stats.gamma.rvs(a, scale=scale, size=size)

    x = []
    for aidx, scaleidx in zip(np.nditer(a), np.nditer(scale)):
      x += [stats.gamma.rvs(aidx, scale=scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x


class Geom(Distribution):
  """Geometric distribution.
  """
  def __init__(self):
    super(Geom, self).__init__(None)

  def rvs(self, p, size=1):
    """Random variates.

    Parameters
    ----------
    p : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`p\in(0,1)`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(p, np.ndarray):
      p = np.asarray(p)
    if len(p.shape) == 0:
      return stats.geom.rvs(p, size=size)

    x = []
    for pidx in np.nditer(p):
      x += [stats.geom.rvs(pidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpmf(self, x, p):
    """Log of the probability mass function.
    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    p : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`p\in(0,1)`.
    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    x = tf.cast(x, dtype=tf.float32)
    p = tf.cast(p, dtype=tf.float32)
    return (x - 1) * tf.log(1.0 - p) + tf.log(p)


class InverseGamma(Distribution):
  """Inverse Gamma distribution.

  Shape/scale parameterization (typically denoted: :math:`(k, \\theta)`)
  """
  def __init__(self):
    super(InverseGamma, self).__init__(distributions.InverseGamma)

  def rvs(self, a, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    a : float or np.ndarray
      **Shape** parameter. 0-D or 1-D tensor, with all elements
      constrained to :math:`a > 0`.
    scale : float or np.ndarray
      **Scale** parameter. 0-D or 1-D tensor, with all elements
      constrained to :math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(a, np.ndarray):
      a = np.asarray(a)
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(a.shape) == 0:
      return stats.invgamma.rvs(a, scale=scale, size=size)

    x = []
    for aidx, scaleidx in zip(np.nditer(a), np.nditer(scale)):
      x += [stats.invgamma.rvs(aidx, scale=scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()

    # This is temporary to avoid returning Inf values.
    x[x < 1e-10] = 0.1
    x[x > 1e10] = 1.0
    x[np.logical_not(np.isfinite(x))] = 1.0
    return x


class Laplace(Distribution):
  """Laplace distribution.
  """
  def __init__(self):
    super(Laplace, self).__init__(distributions.Laplace)


class LogNorm(Distribution):
  """LogNormal distribution.
  """
  def __init__(self):
    super(LogNorm, self).__init__(None)

  def rvs(self, s, size=1):
    """Random variates.

    Parameters
    ----------
    s : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`s > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(s, np.ndarray):
      s = np.asarray(s)
    if len(s.shape) == 0:
      return stats.lognorm.rvs(s, size=size)

    x = []
    for sidx in np.nditer(s):
      x += [stats.lognorm.rvs(sidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpdf(self, x, s):
    """Log of the probability density function.
    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    s : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`s > 0`.
    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    x = tf.cast(x, dtype=tf.float32)
    s = tf.cast(s, dtype=tf.float32)
    return -0.5 * tf.log(2 * np.pi) - tf.log(s) - tf.log(x) - \
        0.5 * tf.square(tf.log(x) / s)


class Multinomial(Distribution):
  """Multinomial distribution.

  Note: there is no equivalent version implemented in SciPy.
  """
  def __init__(self):
    super(Multinomial, self).__init__(None)

  def rvs(self, n, p, size=1):
    """Random variates.

    Parameters
    ----------
    n : int or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`n > 0`.
    p : np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`\sum_i p_k = 1`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if len(p.shape) == 1:
      # np.random.multinomial defaults to (size x p.shape)
      return np.random.multinomial(n, p, size=size)

    if not isinstance(n, np.ndarray):
      n = np.asarray(n)

    x = []
    # This doesn't work for non-matrix parameters.
    for nidx, prow in zip(n, p):
      x += [np.random.multinomial(nidx, prow, size=size)]

    # This only works for rank 3 tensor.
    x = np.rollaxis(np.asarray(x), 1)
    return x

  def logpmf(self, x, n, p):
    """Log of the probability mass function.
    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor for n > 1, where the inner (right-most)
      dimension represents the multivariate dimension. Each
      element is the number of outcomes in a bucket and not a
      one-hot.
    n : tf.Tensor
      A tensor of one less dimension than ``x``,
      representing the number of outcomes, equal to sum x[i]
      along the inner (right-most) dimension.
    p : tf.Tensor
      A tensor of one less dimension than ``x``, representing
      probabilities which sum to 1.
    Returns
    -------
    tf.Tensor
      A tensor of one dimension less than the input.
    """
    x = tf.cast(x, dtype=tf.float32)
    n = tf.cast(n, dtype=tf.float32)
    p = tf.cast(p, dtype=tf.float32)
    multivariate_idx = len(get_dims(x)) - 1
    if multivariate_idx == 0:
      return tf.lgamma(n + 1.0) - \
          tf.reduce_sum(tf.lgamma(x + 1.0)) + \
          tf.reduce_sum(x * tf.log(p))
    else:
      return tf.lgamma(n + 1.0) - \
          tf.reduce_sum(tf.lgamma(x + 1.0), multivariate_idx) + \
          tf.reduce_sum(x * tf.log(p), multivariate_idx)

  def entropy(self, n, p):
    """TODO
    """
    # Note that given n and p where p is a probability vector of
    # length k, the entropy requires a sum over all
    # possible configurations of a k-vector which sums to n. It's
    # expensive.
    # http://stackoverflow.com/questions/36435754/generating-a-numpy-array-with-all-combinations-of-numbers-that-sum-to-less-than
    sess = tf.Session()
    n = sess.run(tf.cast(tf.squeeze(n), dtype=tf.int32))
    sess.close()
    p = tf.cast(tf.squeeze(p), dtype=tf.float32)
    if isinstance(n, np.int32):
      k = get_dims(p)[0]
      max_range = np.zeros(k, dtype=np.int32) + n
      x = np.array([i for i in product(*(range(i + 1) for i in max_range))
                    if sum(i) == n])
      logpmf = self.logpmf(x, n, p)
      return tf.reduce_sum(tf.exp(logpmf) * logpmf)
    else:
      out = []
      for j in range(n.shape[0]):
        k = get_dims(p)[0]
        max_range = np.zeros(k, dtype=np.int32) + n[j]
        x = np.array([i for i in product(*(range(i + 1) for i in max_range))
                      if sum(i) == n[j]])
        logpmf = self.logpmf(x, n[j], p[j, :])
        out += [tf.reduce_sum(tf.exp(logpmf) * logpmf)]

      return tf.pack(out)


class MultivariateNormalDiag(Distribution):
  """Multivariate Normal (with diagonal covariance) distribution.
  """
  def __init__(self):
    super(MultivariateNormalDiag, self).__init__(
        distributions.MultivariateNormalDiag)


class MultivariateNormalCholesky(Distribution):
  """Multivariate Normal (with Cholesky factorized covariance)  distribution.
  """
  def __init__(self):
    super(MultivariateNormalCholesky, self).__init__(
        distributions.MultivariateNormalCholesky)


class MultivariateNormalFull(Distribution):
  """Multivariate Normal (with full rank covariance) distribution.
  """
  def __init__(self):
    super(MultivariateNormalFull, self).__init__(
        distributions.MultivariateNormalFull)

  def rvs(self, mean=None, cov=1, size=1):
    """Random variates.

    Parameters
    ----------
    mean : np.ndarray, optional
      1-D tensor. Defaults to zero mean.
    cov : np.ndarray, optional
      1-D or 2-D tensor. Defaults to identity matrix.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if len(mean.shape) == 1:
      x = stats.multivariate_normal.rvs(mean, cov, size=size)
      # stats.multivariate_normal.rvs returns (size, ) if
      # mean has shape (1,). Expand last dimension.
      if mean.shape[0] == 1:
        x = np.expand_dims(x, axis=-1)
      # stats.multivariate_normal.rvs returns (size x shape) if
      # size > 1, and shape if size == 1. Expand first dimension.
      if size == 1:
        x = np.expand_dims(x, axis=0)

      return x

    x = []
    # This doesn't work for non-matrix parameters.
    for meanrow, covmat in zip(mean, cov):
      x += [stats.multivariate_normal.rvs(meanrow, covmat, size=size)]

    # This only works for rank 3 tensor.
    x = np.rollaxis(np.asarray(x), 1)
    return x


class NBinom(Distribution):
  """Negative binomial distribution.
  """
  def __init__(self):
    super(NBinom, self).__init__(None)

  def rvs(self, n, p, size=1):
    """Random variates.

    Parameters
    ----------
    n : int or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`n > 0`.
    p : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`p\in(0,1)`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(n, np.ndarray):
      n = np.asarray(n)
    if not isinstance(p, np.ndarray):
      p = np.asarray(p)
    if len(n.shape) == 0:
      return stats.nbinom.rvs(n, p, size=size)

    x = []
    for nidx, pidx in zip(np.nditer(n), np.nditer(p)):
      x += [stats.nbinom.rvs(nidx, pidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpmf(self, x, n, p):
    """Log of the probability mass function.

    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    n : int
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`n > 0`.
    p : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`p\in(0,1)`.

    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    x = tf.cast(x, dtype=tf.float32)
    n = tf.cast(n, dtype=tf.float32)
    p = tf.cast(p, dtype=tf.float32)
    return tf.lgamma(x + n) - tf.lgamma(x + 1.0) - tf.lgamma(n) + \
        n * tf.log(p) + x * tf.log(1.0 - p)


class Normal(Distribution):
  """Normal (Gaussian) distribution.
  """
  def __init__(self):
    super(Normal, self).__init__(distributions.Normal)

  def rvs(self, loc=0, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    loc : float or np.ndarray
      0-D or 1-D tensor.
    scale : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(loc, np.ndarray):
      loc = np.asarray(loc)
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(loc.shape) == 0:
      return stats.norm.rvs(loc, scale, size=size)

    x = []
    for locidx, scaleidx in zip(np.nditer(loc), np.nditer(scale)):
      x += [stats.norm.rvs(locidx, scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x


class Poisson(Distribution):
  """Poisson distribution.
  """
  def __init__(self):
    super(Poisson, self).__init__(None)

  def rvs(self, mu, size=1):
    """Random variates.

    Parameters
    ----------
    mu : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`mu > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(mu, np.ndarray):
      mu = np.asarray(mu)
    if len(mu.shape) == 0:
      return stats.poisson.rvs(mu, size=size)

    x = []
    for muidx in np.nditer(mu):
      x += [stats.poisson.rvs(muidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpmf(self, x, mu):
    """Log of the probability mass function.
    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    mu : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`mu > 0`.
    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    x = tf.cast(x, dtype=tf.float32)
    mu = tf.cast(mu, dtype=tf.float32)
    return x * tf.log(mu) - mu - tf.lgamma(x + 1.0)


class StudentT(Distribution):
  """Student-t distribution.
  """
  def __init__(self):
    super(StudentT, self).__init__(distributions.StudentT)

  def rvs(self, df, loc=0, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    df : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`df > 0`.
    loc : float or np.ndarray
      0-D or 1-D tensor.
    scale : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(df, np.ndarray):
      df = np.asarray(df)
    if not isinstance(loc, np.ndarray):
      loc = np.asarray(loc)
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(df.shape) == 0:
      return stats.t.rvs(df, loc=loc, scale=scale, size=size)

    x = []
    for dfidx, locidx, scaleidx in zip(np.nditer(df),
                                       np.nditer(loc),
                                       np.nditer(scale)):
      x += [stats.t.rvs(dfidx, loc=locidx, scale=scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x


class TruncNorm(Distribution):
  """Truncated Normal (Gaussian) distribution.
  """
  def __init__(self):
    super(TruncNorm, self).__init__(None)

  def rvs(self, a, b, loc=0, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    a : float or np.ndarray
      Left boundary, with respect to the standard normal.
      0-D or 1-D tensor.
    b : float or np.ndarray
      Right boundary, with respect to the standard normal.
      0-D or 1-D tensor, and with ``b > a`` element-wise.
    loc : float or np.ndarray
      0-D or 1-D tensor.
    scale : float or np.ndarray
      0-D or 1-D tensor, with all elements constrained to
      :math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(a, np.ndarray):
      a = np.asarray(a)
    if not isinstance(b, np.ndarray):
      b = np.asarray(b)
    if not isinstance(loc, np.ndarray):
      loc = np.asarray(loc)
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(a.shape) == 0:
      return stats.truncnorm.rvs(a, b, loc, scale, size=size)

    x = []
    for aidx, bidx, locidx, scaleidx in zip(np.nditer(a),
                                            np.nditer(b),
                                            np.nditer(loc),
                                            np.nditer(scale)):
      x += [stats.truncnorm.rvs(aidx, bidx, locidx, scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x

  def logpdf(self, x, a, b, loc=0, scale=1):
    """Log of the probability density function.

    Parameters
    ----------
    x : tf.Tensor
      A n-D tensor.
    a : tf.Tensor
      Left boundary, with respect to the standard normal.
      A tensor of same shape as ``x``.
    b : tf.Tensor
      Right boundary, with respect to the standard normal.
      A tensor of same shape as ``x``, and with ``b > a``
      element-wise.
    loc : tf.Tensor
      A tensor of same shape as ``x``.
    scale : tf.Tensor
      A tensor of same shape as ``x``, and with all elements
      constrained to :math:`scale > 0`.

    Returns
    -------
    tf.Tensor
      A tensor of same shape as input.
    """
    # Note there is no error checking if x is outside domain.
    x = tf.cast(x, dtype=tf.float32)
    # This is slow, as we require use of stats.norm.cdf.
    sess = tf.Session()
    a = sess.run(tf.cast(a, dtype=tf.float32))
    b = sess.run(tf.cast(b, dtype=tf.float32))
    loc = sess.run(tf.cast(loc, dtype=tf.float32))
    scale = sess.run(tf.cast(scale, dtype=tf.float32))
    sess.close()
    return -tf.log(scale) + norm.logpdf(x, loc, scale) - \
        tf.log(tf.cast(stats.norm.cdf((b - loc) / scale) -
               stats.norm.cdf((a - loc) / scale), dtype=tf.float32))


class Uniform(Distribution):
  """Uniform distribution (continous)

  This distribution is constant between [`a`, `b`], and 0 elsewhere.
  """
  def __init__(self):
    super(Uniform, self).__init__(distributions.Uniform)

  def rvs(self, loc=0, scale=1, size=1):
    """Random variates.

    Parameters
    ----------
    loc : float or np.ndarray
      Left boundary. 0-D or 1-D tensor.
    scale : float or np.ndarray
      Width of distribution. 0-D or 1-D tensor, with all
      elements constrained to math:`scale > 0`.
    size : int
      Number of random variable samples to return.

    Returns
    -------
    np.ndarray
      A np.ndarray of dimensions size x shape.
    """
    if not isinstance(loc, np.ndarray):
      loc = np.asarray(loc)
    if not isinstance(scale, np.ndarray):
      scale = np.asarray(scale)
    if len(loc.shape) == 0:
      return stats.uniform.rvs(loc, scale, size=size)

    x = []
    for locidx, scaleidx in zip(np.nditer(loc), np.nditer(scale)):
      x += [stats.uniform.rvs(locidx, scaleidx, size=size)]

    # Note this doesn't work for multi-dimensional sizes.
    x = np.asarray(x).transpose()
    return x


bernoulli = Bernoulli()
beta = Beta()
binom = Binom()
categorical = Categorical()
chi2 = Chi2()
dirichlet = Dirichlet()
dirichlet_multinomial = DirichletMultinomial()
exponential = Exponential()
gamma = Gamma()
geom = Geom()
inverse_gamma = InverseGamma()
laplace = Laplace()
lognorm = LogNorm()
multinomial = Multinomial()
multivariate_normal_diag = MultivariateNormalDiag()
multivariate_normal_cholesky = MultivariateNormalCholesky()
multivariate_normal_full = MultivariateNormalFull()
nbinom = NBinom()
normal = Normal()
poisson = Poisson()
studentt = StudentT()
truncnorm = TruncNorm()
uniform = Uniform()

# for backwards naming compatibility with scipy.stats
expon = exponential
norm = normal
invgamma = inverse_gamma
t = studentt
multivariate_normal = multivariate_normal_full
