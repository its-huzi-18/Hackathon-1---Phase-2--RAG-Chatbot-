import type {ReactNode} from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container text--center">
        <div className={styles.heroLogoContainer}>
          <img
            src="/img/logo-professional.svg"
            alt="Advanced Robotics & AI Logo"
            className={styles.heroLogo}
          />
        </div>
        <Heading as="h1" className="hero__title">
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Explore Documentation - 5min ⏱️
          </Link>
        </div>
      </div>
    </header>
  );
}

function Features(): ReactNode {
  const features = [
    {
      title: 'Advanced Robotics',
      description: 'Cutting-edge humanoid robotics technology with precise motor control and environmental awareness.',
      imageUrl: '/img/undraw_docusaurus_mountain.svg',
    },
    {
      title: 'AI Integration',
      description: 'Sophisticated artificial intelligence systems that enable autonomous decision-making and learning.',
      imageUrl: '/img/undraw_docusaurus_tree.svg',
    },
    {
      title: 'Research & Development',
      description: 'Ongoing innovation in physical AI systems for industrial and personal applications.',
      imageUrl: '/img/undraw_docusaurus_react.svg',
    },
  ];

  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {features.map((feature, idx) => (
            <div className="col col--4" key={idx}>
              <div className="text--center">
                <img src={feature.imageUrl} className={styles.featureImage} alt={feature.title} />
              </div>
              <div className="text--center padding-horiz--md">
                <Heading as="h3">{feature.title}</Heading>
                <p>{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function Home(): ReactNode {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Welcome to ${siteConfig.title}`}
      description="Advanced Robotics & AI - Empowering the next generation of AI and Robotics innovators">
      <HomepageHeader />
      <main>
        <Features />
      </main>
    </Layout>
  );
}
